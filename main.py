import asyncio
import logging
import time
from datetime import datetime
from typing import List, Dict, Optional, Any
import aiohttp
from func import trend_ai
from request_bybit import get_bybit_linear_tickers_usdt

API_BASE_URL = "https://api.bybit.com/v5"
DEFAULT_KLINE_LIMIT = 300
RATE_LIMIT = 50  # requests per second
REQUEST_TIMEOUT = 10

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bybit_data.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AsyncBybitDataCollector:
    def __init__(self):
        self.session = None
        self.request_times = []

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            headers={'User-Agent': 'AsyncBybitDataCollector/1.0'}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _rate_limit(self):
        """Implement rate limiting"""
        now = time.time()
        self.request_times = [t for t in self.request_times if now - t < 1.0]
        if len(self.request_times) >= RATE_LIMIT:
            await asyncio.sleep(0.1)
        self.request_times.append(now)

    async def verify_trading_pair(self, trading_pair: str) -> bool:
        """Verify if trading pair exists on Bybit"""
        await self._rate_limit()
        url = f"{API_BASE_URL}/market/tickers"
        params = {"category": "linear", "symbol": trading_pair}

        try:
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("retCode") == 0 and len(data["result"]["list"]) > 0
        except (aiohttp.ClientError, KeyError) as e:
            logger.error(f"Error verifying {trading_pair}: {str(e)}")
            return False

    async def get_kline_data(self, trading_pair: str, interval: int = 5) -> List[List[str]]:
        """Get kline data for a trading pair"""
        await self._rate_limit()
        url = f"{API_BASE_URL}/market/kline"
        params = {
            "category": "linear",
            "symbol": trading_pair,
            "interval": str(interval),
            "limit": DEFAULT_KLINE_LIMIT
        }

        try:
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()

                if data.get("retCode") != 0:
                    return []

                result = data["result"]["list"][::-1]
                result.append(["Timestamp", "Open", "High", "Low", "Close", "Volume", "Volume in Currency"])
                return result[::-1]

        except (aiohttp.ClientError, KeyError) as e:
            logger.error(f"Error fetching kline data for {trading_pair}: {str(e)}")
            return []

    @staticmethod
    def round_time_down(interval_minutes: int = 5) -> str:
        minutes = datetime.now().minute
        rounded_minutes = (minutes // interval_minutes) * interval_minutes
        rounded_time = datetime.now().replace(minute=rounded_minutes, second=0, microsecond=0)
        return rounded_time.strftime("%Y-%m-%d %H:%M")

    async def process_pair(self, trading_pair: str) -> Optional[Dict[str, Any]]:
        """Process a single trading pair"""
        if not await self.verify_trading_pair(trading_pair):
            logger.error(f"Trading pair {trading_pair} not found")
            return None

        kline_data = await self.get_kline_data(trading_pair)
        if not kline_data:
            return None

        return {
            'ticker': trading_pair,
            'time': self.round_time_down(),
            'kline': kline_data
        }


async def process_pairs(pairs: List[str]) -> List[Dict[str, Any]]:
    """Process multiple trading pairs concurrently"""
    async with AsyncBybitDataCollector() as collector:
        tasks = [collector.process_pair(pair) for pair in pairs]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if isinstance(r, dict)]


async def main():
    try:
        while True:
            trading_pairs = get_bybit_linear_tickers_usdt()
            results = await process_pairs(trading_pairs)

            for result in results:
                print(result)
                if result:
                    try:
                        ai = trend_ai(result)
                        print(ai)
                        if ai and ai[0] != '0' and len(ai) == 4:
                            old_value = float(ai[1])
                            new_value = float(ai[2])
                            percent = round(abs(((new_value - old_value) / old_value) * 100), 2)
                            ai.append(percent)
                            logger.info(f"Entry point found for {result['ticker']}: {ai}")
                        else:
                            logger.debug(f"No entry points for {result['ticker']}")
                    except Exception as e:
                        logger.error(f"Error processing AI data for {result['ticker']}: {e}")

            await asyncio.sleep(60)  # Wait before next iteration

    except KeyboardInterrupt:
        logger.info("Shutting down...")


if __name__ == "__main__":
    asyncio.run(main())