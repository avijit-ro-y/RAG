"""
Test datasets and ground truth for RAG evaluation
"""

EVALUATION_QUERIES = [
    {
        "query": "What are the main tourist attractions in Kerala?",
        "relevant_states": ["Kerala"],
        "ground_truth": "Kerala is famous for its backwaters in Alleppey and Kumarakom, hill stations like Munnar and Wayanad, beaches such as Kovalam and Varkala, the Periyar Wildlife Sanctuary in Thekkady, and cultural experiences including Kathakali performances and Ayurvedic treatments. The state is also known for its spice plantations and houseboat cruises.",
        "difficulty": "easy"
    },
    {
        "query": "Tell me about the history of Tamil Nadu",
        "relevant_states": ["Tamil Nadu"],
        "ground_truth": "Tamil Nadu has ancient Tamil kingdoms like Cholas, Cheras, and Pandyas. The Chola dynasty was notable for maritime trade and temple architecture including Brihadeeswarar Temple. The region was influenced by various dynasties and came under British rule before becoming part of independent India.",
        "difficulty": "medium"
    },
    {
        "query": "What is the economy of Gujarat like?",
        "relevant_states": ["Gujarat"],
        "ground_truth": "Gujarat has one of India's most industrialized economies known for textiles chemicals petrochemicals engineering and diamond cutting. It is a major port state with significant contribution to India's exports.",
        "difficulty": "medium"
    },
    {
        "query": "Which states are known for their desert landscapes?",
        "relevant_states": ["Rajasthan", "Gujarat"],
        "ground_truth": "Rajasthan is known for the Thar Desert with cities like Jaisalmer Bikaner and Jodhpur. Gujarat has desert regions in Kutch district known for the Rann of Kutch salt desert.",
        "difficulty": "hard"
    },
    {
        "query": "What are the geographical features of Himachal Pradesh?",
        "relevant_states": ["Himachal Pradesh"],
        "ground_truth": "Himachal Pradesh is located in the Himalayas with high mountain peaks valleys rivers and hill stations. It is known for scenic beauty snow-capped mountains and adventure tourism.",
        "difficulty": "easy"
    },
    {
        "query": "Which states have significant coastal areas and maritime activities?",
        "relevant_states": ["Kerala", "Tamil Nadu", "Gujarat", "Maharashtra", "Karnataka", "Andhra Pradesh", "Odisha", "West Bengal"],
        "ground_truth": "Indian coastal states include Kerala Tamil Nadu Gujarat Maharashtra Karnataka Andhra Pradesh Odisha and West Bengal each with important ports and maritime industries.",
        "difficulty": "hard"
    },
    {
        "query": "Describe the culture and traditions of Rajasthan",
        "relevant_states": ["Rajasthan"],
        "ground_truth": "Rajasthan is known for vibrant culture including folk dances like Ghoomar colorful festivals traditional music handicrafts royal heritage with palaces and forts and distinctive cuisine.",
        "difficulty": "medium"
    },
    {
        "query": "What are the main agricultural products of Punjab?",
        "relevant_states": ["Punjab"],
        "ground_truth": "Punjab is known as India's breadbasket primarily producing wheat rice cotton and sugarcane. It is a major contributor to India's food grain production.",
        "difficulty": "easy"
    },
    {
        "query": "Which states are part of the Seven Sister States in Northeast India?",
        "relevant_states": ["Arunachal Pradesh", "Assam", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Tripura"],
        "ground_truth": "The Seven Sister States of Northeast India are Arunachal Pradesh Assam Manipur Meghalaya Mizoram Nagaland and Tripura known for diverse cultures and natural beauty.",
        "difficulty": "hard"
    },
    {
        "query": "What is the capital of Maharashtra and its significance?",
        "relevant_states": ["Maharashtra"],
        "ground_truth": "Mumbai is the capital of Maharashtra and India's financial capital home to stock exchanges major banks and Bollywood film industry. It is also a major port city.",
        "difficulty": "easy"
    }
]

HALLUCINATION_QUERIES = [
    {
        "query": "Tell me about the space program of Goa",
        "expected_hallucination": True,
        "reason": "Goa doesn't have a significant space program - this should trigger hallucination detection"
    },
    {
        "query": "What are the snow-capped mountains in Kerala?",
        "expected_hallucination": True,
        "reason": "Kerala doesn't have snow-capped mountains due to its tropical climate"
    },
    {
        "query": "Describe the desert safari opportunities in West Bengal",
        "expected_hallucination": True,
        "reason": "West Bengal has deltaic geography with rivers and forests, not deserts"
    },
    {
        "query": "Tell me about the penguin colonies in Maharashtra",
        "expected_hallucination": True,
        "reason": "Penguins don't naturally exist in Maharashtra's climate"
    }
]