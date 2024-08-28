import os
import logging
import random
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Define states
CHOOSING, READING, QUIZZING = range(3)

# Define lesson content
lessons = {
    'intro': [
        "Aptos is a Layer 1 blockchain built with safety and user experience as key priorities.",
        "It was founded by former members of the Diem project at Meta (formerly Facebook).",
        "Aptos aims to be the most safe and scalable Layer 1 blockchain.",
        "The blockchain uses a novel smart contract language called Move for added security and flexibility."
    ],
    'features': [
        "Key features of Aptos include:",
        "1. Move programming language: Designed for safe and flexible asset management.",
        "2. Parallel execution engine: Allows for high transaction throughput.",
        "3. Modular architecture: Enables easy upgrades and improvements.",
        "4. Strong focus on security: Implements various measures to prevent common blockchain vulnerabilities."
    ],
    'start_guide': [
        "Welcome to 'Getting Started with Aptos'! Let's begin your journey into the Aptos ecosystem.",
        
        "Step 1: Set up an Aptos Wallet\n"
        "- Visit the official Petra Wallet website (https://petra.app)\n"
        "- Download and install the Petra browser extension on browser or mobile app\n"
        "- Create a new wallet and securely store your seed phrase",

        "Step 1.5: Set up an Aptos Connect wallet\n"
        "- Visit the official Aptos Connect website (https://aptosconnect.app/)\n"
        "- Make an account without the need for a seed phrase or private key\n"
        "- Enjoy the benefits of Aptos Connect and Keyless accounts",
        
        
        "Step 2: Acquire Some APT Tokens\n"
        "- For testnet: Use the Aptos Faucet to get free testnet tokens\n"
        "- For mainnet: Acquire APT from a supported centralized or decentralized cryptocurrency exchange",
        
        "Step 3: Explore Aptos Explorer\n"
        "- Visit https://explorer.aptoslabs.com\n"
        "- Use it to view transactions, accounts, analytics, and network activity",
        
        "Step 4: Join the Aptos Community\n"
        "- Follow Aptos on X (https://x.com/Aptos)\n"
        "- Aptos is global.  Check out the regional communities (https://link3.to/aptos_community)\n"
        "- Join the official Discord server and Telegram group for discussions and support",
        
        "Step 5: Learn about Move Programming\n"
        "- Familiarize yourself with the Move language documentation (https://aptos.dev/) \n"
        "- Try out some basic Move tutorials on the Aptos Learn website (https://learn.aptoslabs.com/)",
        
        "Congratulations! You've taken your first steps into the Aptos ecosystem. Continue exploring to learn more about Aptos's features and capabilities."
    ],
    'basic_ops': [
        "Welcome to Basic Operations on Aptos! Let's explore the fundamental actions you can perform on the Aptos blockchain.",

        "1. Sending Transactions\n"
        "- Open your Petra or Aptos Connect wallet\n"
        "- Select 'Send' and enter the recipient's address\n"
        "- Specify the amount of APT to send\n"
        "- Review the transaction details and confirm\n"
        "- Wait for the transaction to be processed and confirmed on the blockchain",

        "2. Exploring and Interacting with NFTs\n"
        "- NFTs (Non-Fungible Tokens) on Aptos represent unique digital assets\n"
        "- Browse NFT marketplaces like Topaz or BlueMove to explore Aptos NFTs\n"
        "- Connect your Aptos wallet to these platforms to buy, sell, or trade NFTs\n"
        "- You can also mint NFTs through various Aptos-based NFT projects\n"
        "- Store your NFTs securely in your Aptos wallet\n"
        "- View your NFT collection in your wallet or on NFT explorer platforms",

        "3. Staking APT\n"
        "- Staking allows you to earn rewards by supporting network security\n"
        "- Choose a validator node to stake with\n"
        "- Use your wallet or the Aptos staking interface to delegate your APT\n"
        "- Monitor your staking rewards through the Aptos Explorer",

        "4. Participating in Governance\n"
        "- Aptos uses on-chain governance for protocol upgrades and parameter changes\n"
        "- Review active proposals on the Aptos Governance platform\n"
        "- Cast your vote using your staked APT\n"
        "- Follow the outcome and implementation of passed proposals",

        "5. Using Aptos Name Service (ANS)\n"
        "- ANS allows you to register human-readable names for your Aptos address\n"
        "- Visit the ANS website and connect your wallet\n"
        "- Search for and register an available name\n"
        "- Use your .apt name instead of your long address for transactions",

        "6. Exploring DeFi on Aptos\n"
        "- Aptos has a growing DeFi ecosystem\n"
        "- You can swap tokens, provide liquidity, or participate in yield farming\n"
        "- Always research protocols thoroughly and understand the risks involved",

        "Remember, always double-check addresses, transaction details, and contract interactions to ensure the security of your assets on Aptos."
    ],
    'advanced': [
        "Welcome to Advanced Topics in Aptos! Let's explore some of the more complex aspects of the Aptos blockchain.",

        "1. Move Programming Language\n"
        "- Move is the smart contract language used in Aptos\n"
        "- Key features: resource-oriented programming, static typing, and formal verification\n"
        "- Resources in Move are used to represent assets, ensuring they can't be copied or discarded\n"
        "- Move modules are reusable libraries of code, while scripts are executable transaction logic\n"
        "- The Move VM executes Move bytecode, providing a secure runtime environment",

        "2. Parallel Execution Engine\n"
        "- Aptos uses a novel parallel execution engine called Block-STM\n"
        "- It allows for concurrent execution of transactions, significantly improving throughput\n"
        "- Block-STM works by speculatively executing transactions in parallel\n"
        "- If conflicts are detected, it automatically retries affected transactions\n"
        "- This approach can achieve near-linear scalability with the number of CPU cores",

        "3. Consensus Mechanism\n"
        "- Aptos uses a Delegated Proof-of-Stake (DPoS) consensus mechanism\n"
        "- Validators are responsible for proposing and voting on blocks\n"
        "- The Byzantine Fault Tolerance (BFT) algorithm ensures consensus even if some validators are malicious\n"
        "- In Aptos' BFT, consensus is reached when more than 2/3 of validators agree on a block\n"
        "- This mechanism provides fast finality and high throughput",

        "4. Aptos Governance\n"
        "- Aptos uses an on-chain governance model for protocol upgrades and parameter changes\n"
        "- AIP (Aptos Improvement Proposals) are formal documents proposing changes to the protocol\n"
        "- APT token holders can vote on AIPs, with voting power proportional to their stake\n"
        "- Approved proposals are automatically implemented through smart contracts\n"
        "- This system ensures decentralized decision-making and protocol evolution",

        "5. Layer 2 Solutions and Scalability\n"
        "- While Aptos is highly scalable, Layer 2 solutions can further enhance its capabilities\n"
        "- Sharding is a potential scalability solution, where the network is divided into smaller parts\n"
        "- In Aptos, sharding could involve splitting the state and transaction processing across multiple chains\n"
        "- This would allow for even greater parallelism and throughput\n"
        "- Other Layer 2 solutions like rollups or state channels could also be implemented on Aptos",

        "6. Interoperability\n"
        "- Interoperability allows Aptos to communicate with other blockchains\n"
        "- Cross-chain bridges enable asset transfers between Aptos and other chains\n"
        "- These bridges typically use smart contracts on both chains to lock and mint assets\n"
        "- Wrapped assets on Aptos represent tokens from other chains (e.g., Wrapped ETH)\n"
        "- Interoperability protocols like LayerZero or Chainlink CCIP could be integrated with Aptos",

        "7. Advanced DeFi Concepts\n"
        "- Flash loans allow users to borrow large amounts without collateral for a single transaction\n"
        "- Yield farming strategies involve moving assets between protocols to maximize returns\n"
        "- Liquidity mining rewards users for providing liquidity to decentralized exchanges\n"
        "- Risks in advanced DeFi include smart contract vulnerabilities, impermanent loss, and market volatility\n"
        "- Opportunities include high yields, arbitrage, and participation in new financial instruments",

        "These advanced topics form the cutting edge of Aptos technology. Understanding them provides deep insight into the Aptos ecosystem."
    ],
    # Add more lessons for 'start_guide', 'basic_ops', and 'advanced'
}

# Define quiz questions
quizzes = {
    'intro': [
        {
            'question': "What is Aptos?",
            'options': ["A Layer 2 scaling solution", "A Layer 1 blockchain", "A cryptocurrency", "A smart contract platform"],
            'correct': 1
        },
        {
            'question': "Who founded Aptos?",
            'options': ["Ethereum developers", "Bitcoin core team", "Former Diem (Facebook) project members", "Independent blockchain enthusiasts"],
            'correct': 2
        }
    ],
    'features': [
        {
            'question': "What programming language does Aptos use for smart contracts?",
            'options': ["Solidity", "Rust", "Move", "Python"],
            'correct': 2
        },
        {
            'question': "Which feature allows Aptos to achieve high transaction throughput?",
            'options': ["Proof of Stake", "Sharding", "Parallel execution engine", "Layer 2 scaling"],
            'correct': 2
        }
    ],
      'start_guide': [
        {
            'question': "What are the two main wallet options for Aptos?",
            'options': ["MetaMask and Trust Wallet", "Petra Wallet and Aptos Connect", "Coinbase Wallet and Ledger", "MyEtherWallet and Trezor"],
            'correct': 1
        },
        {
            'question': "What unique feature does Aptos Connect offer?",
            'options': ["Faster transactions", "Lower fees", "Account creation without seed phrase or private key", "Automatic staking"],
            'correct': 2
        },
        {
            'question': "How can you get free testnet tokens for Aptos?",
            'options': ["Purchase them", "Mine them", "Use the Aptos Faucet", "They're automatically provided"],
            'correct': 2
        },
        {
            'question': "What tool should you use to view Aptos network activity and analytics?",
            'options': ["Aptos Explorer", "Etherscan", "Blockchain.info", "Aptos Wallet"],
            'correct': 0
        },
        {
            'question': "Where can you find Aptos regional communities?",
            'options': ["Meta", "LinkedIn", "Link3", "Reddit"],
            'correct': 2
        },
        {
            'question': "What is the primary programming language used for Aptos smart contracts?",
            'options': ["Solidity", "Python", "JavaScript", "Move"],
            'correct': 3
        },
        {
            'question': "Where can you find official Aptos Move tutorials?",
            'options': ["YouTube", "Stack Overflow", "Aptos Learn", "GitHub"],
            'correct': 2
        },
        {
            'question': "Which social media platform is mentioned for following Aptos updates?",
            'options': ["Facebook", "Instagram", "LinkedIn", "X.com"],
            'correct': 3
        }
    ],
    'basic_ops': [
        {
            'question': "What is the first step in sending a transaction on Aptos?",
            'options': ["Mining APT", "Opening your wallet", "Calling a smart contract", "Registering an ANS name"],
            'correct': 1
        },
        {
            'question': "What can you do with NFTs on Aptos?",
            'options': ["Mine new APT tokens", "Create new blockchains", "Buy, sell, and trade unique digital assets", "Stake for network security"],
            'correct': 2
        },
        {
            'question': "What is the purpose of staking APT?",
            'options': ["To send transactions", "To earn rewards and support network security", "To create smart contracts", "To register a domain name"],
            'correct': 1
        },
        {
            'question': "How does Aptos handle protocol upgrades and parameter changes?",
            'options': ["Through off-chain voting", "By developer decisions only", "Using on-chain governance", "Automatically without user input"],
            'correct': 2
        },
        {
            'question': "What does ANS stand for in the Aptos ecosystem?",
            'options': ["Aptos Network Security", "Automated Node System", "Aptos Name Service", "Advanced Notification Service"],
            'correct': 2
        },
        {
            'question': "What can you do with DeFi on Aptos?",
            'options': ["Mine new APT tokens", "Swap tokens and provide liquidity", "Create new blockchains", "Register validator nodes"],
            'correct': 1
        },
        {
            'question': "What should you always do before confirming a transaction on Aptos?",
            'options': ["Close your wallet", "Double-check addresses and details", "Transfer all your APT to another wallet", "Create a new account"],
            'correct': 1
        }
    ],
    'advanced': [
        {
            'question': "In Move programming, what are resources used to represent?",
            'options': ["Functions", "Variables", "Assets", "Loops"],
            'correct': 2
        },
        {
            'question': "How does Block-STM handle transaction conflicts?",
            'options': ["It cancels all transactions", "It automatically retries affected transactions", "It ignores conflicts", "It requires manual resolution"],
            'correct': 1
        },
        {
            'question': "In Aptos' BFT consensus, what percentage of validators must agree for consensus?",
            'options': ["More than 50%", "Exactly 66%", "More than 2/3", "100%"],
            'correct': 2
        },
        {
            'question': "How are approved Aptos Improvement Proposals (AIPs) implemented?",
            'options': ["Manually by developers", "Through community voting", "Automatically through smart contracts", "By validator nodes"],
            'correct': 2
        },
        {
            'question': "What is a potential benefit of sharding in Aptos?",
            'options': ["Reduced security", "Greater parallelism and throughput", "Simpler consensus mechanism", "Lower hardware requirements"],
            'correct': 1
        },
        {
            'question': "How do cross-chain bridges typically work?",
            'options': ["By physically moving assets between chains", "Using smart contracts to lock and mint assets", "Through centralized exchanges", "By converting all assets to a common currency"],
            'correct': 1
        },
        {
            'question': "What is a unique characteristic of flash loans in DeFi?",
            'options': ["They require high collateral", "They last for months", "They allow borrowing without collateral for a single transaction", "They have very low interest rates"],
            'correct': 2
        }
    ],
    # Add more quizzes for other topics
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"User {update.effective_user.id} started the bot")
    await send_main_menu(update, context)
    return CHOOSING

async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Introduction to Aptos", callback_data='intro')],
        [InlineKeyboardButton("Key Features", callback_data='features')],
        [InlineKeyboardButton("Getting Started", callback_data='start_guide')],
        [InlineKeyboardButton("Basic Operations", callback_data='basic_ops')],
        [InlineKeyboardButton("Advanced Topics", callback_data='advanced')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = "Welcome to the Aptos Educational Bot! I'm here to help you learn about the Aptos blockchain. What would you like to learn about?"
    
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text(message_text, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    logger.info(f"User {update.effective_user.id} pressed button: {query.data}")

    if query.data == 'menu':
        await send_main_menu(update, context)
        return CHOOSING
    elif query.data in lessons:
        context.user_data['lesson'] = query.data
        context.user_data['lesson_index'] = 0
        context.user_data['quiz_index'] = 0
        context.user_data['score'] = 0
        await send_lesson(update, context)
        return READING
    else:
        await query.message.reply_text("I'm sorry, that option isn't available yet.")
        return CHOOSING

async def send_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lesson = context.user_data['lesson']
    index = context.user_data['lesson_index']
    
    if index < len(lessons[lesson]):
        keyboard = [[InlineKeyboardButton("Next", callback_data='next')]]
        if index > 0:
            keyboard[0].insert(0, InlineKeyboardButton("Previous", callback_data='prev'))
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.message.edit_text(
            lessons[lesson][index],
            reply_markup=reply_markup
        )
        return READING
    else:
        await update.callback_query.message.edit_text(
            "You've completed this lesson! Let's test your knowledge with a quiz.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Start Quiz", callback_data='start_quiz')]])
        )
        return QUIZZING

async def navigate_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'next':
        context.user_data['lesson_index'] += 1
    elif query.data == 'prev':
        context.user_data['lesson_index'] -= 1
    elif query.data == 'menu':
        await send_main_menu(update, context)
        return CHOOSING

    return await send_lesson(update, context)

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    return await send_quiz_question(update, context)

async def send_quiz_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lesson = context.user_data['lesson']
    index = context.user_data['quiz_index']
    
    if index < len(quizzes[lesson]):
        question = quizzes[lesson][index]
        keyboard = [[InlineKeyboardButton(opt, callback_data=f'quiz_{i}') for i, opt in enumerate(question['options'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.message.edit_text(
            f"Question {index + 1}: {question['question']}",
            reply_markup=reply_markup
        )
        return QUIZZING
    else:
        score = context.user_data['score']
        total = len(quizzes[lesson])
        await update.callback_query.message.edit_text(
            f"Quiz completed! Your score: {score}/{total}\n"
            "Choose another topic to continue learning.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Menu", callback_data='menu')]])
        )
        return CHOOSING

async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    lesson = context.user_data['lesson']
    index = context.user_data['quiz_index']
    question = quizzes[lesson][index]
    
    user_answer = int(query.data.split('_')[1])
    if user_answer == question['correct']:
        context.user_data['score'] += 1
        await query.message.reply_text("Correct!")
    else:
        await query.message.reply_text(f"Sorry, the correct answer was: {question['options'][question['correct']]}")
    
    context.user_data['quiz_index'] += 1
    return await send_quiz_question(update, context)

def main() -> None:
    logger.info("Starting bot...")
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [CallbackQueryHandler(button)],
            READING: [CallbackQueryHandler(navigate_lesson)],
            QUIZZING: [
                CallbackQueryHandler(start_quiz, pattern='^start_quiz$'),
                CallbackQueryHandler(handle_quiz_answer, pattern='^quiz_'),
                CallbackQueryHandler(button, pattern='^menu$'),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()