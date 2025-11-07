from telethon import TelegramClient, events
from telethon.tl.types import UpdatePendingJoinRequests
from telethon.tl.functions.channels import InviteToChannelRequest
import asyncio
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Create Telegram client
client = TelegramClient('auto_approve_bot', API_ID, API_HASH)

async def approve_user_request(user_id):
    """Approve user join request by inviting to channel"""
    logger.info(f"🔄 Processing join request for user {user_id}")
    
    try:
        # Get user information
        user = await client.get_entity(user_id)
        logger.info(f"👤 Found user: {user.first_name}")
        
        # Get channel information
        channel = await client.get_entity(CHANNEL_ID)
        logger.info(f"📢 Channel: {channel.title}")
        
        # Invite user to channel (this automatically approves the request)
        logger.info("📨 Sending invitation...")
        await client(InviteToChannelRequest(
            channel=channel,
            users=[user]
        ))
        
        logger.info(f"✅ SUCCESS: Join request from {user.first_name} approved!")
        return True
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ Error approving user {user_id}: {error_msg}")
        
        # Analyze error type
        if "USER_ALREADY_PARTICIPANT" in error_msg:
            logger.info("ℹ️ User is already in the channel")
        elif "USER_PRIVACY_RESTRICTED" in error_msg:
            logger.error("🔒 User has restricted invitations")
        elif "CHAT_ADMIN_REQUIRED" in error_msg:
            logger.error("⚠️ Insufficient administrator rights")
        else:
            logger.error(f"🚨 Unknown error: {error_msg}")
            
        return False

@client.on(events.Raw)
async def handle_join_requests(event):
    """Handle join request events"""
    if isinstance(event, UpdatePendingJoinRequests):
        logger.info("🎯 JOIN REQUEST EVENT DETECTED!")
        logger.info(f"   Channel ID: {event.peer.channel_id}")
        logger.info(f"   Pending requests: {event.requests_pending}")
        logger.info(f"   User IDs: {event.recent_requesters}")
        
        # Check if this is our channel and there are pending requests
        if event.peer.channel_id == CHANNEL_ID and event.requests_pending > 0:
            logger.info("🔄 Starting request processing...")
            
            approved_count = 0
            # Approve all users from recent_requesters
            for user_id in event.recent_requesters:
                if await approve_user_request(user_id):
                    approved_count += 1
                # Pause between processing to avoid rate limits
                await asyncio.sleep(1)
            
            logger.info(f"📊 Result: Approved {approved_count} out of {len(event.recent_requesters)} requests")

async def main():
    """Main bot function"""
    await client.start()
    logger.info("🤖 Bot started and ready to work!")
    
    channel = await client.get_entity(CHANNEL_ID)
    logger.info(f"📢 Monitoring channel: {channel.title}")
    
    logger.info("🎯 Waiting for new join requests...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())