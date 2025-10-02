"""
Icon Template Library for Browser Profile Icons
Pre-designed templates for common use cases
"""

ICON_TEMPLATES = {
    "work": {
        "name": "Work",
        "icon": "💼",
        "color": "#2196F3",
        "gradient": ["#2196F3", "#1976D2"],
        "category": "professional"
    },
    "personal": {
        "name": "Personal",
        "icon": "🏠",
        "color": "#4CAF50",
        "gradient": ["#4CAF50", "#388E3C"],
        "category": "personal"
    },
    "development": {
        "name": "Development",
        "icon": "💻",
        "color": "#FF9800",
        "gradient": ["#FF9800", "#F57C00"],
        "category": "professional"
    },
    "gaming": {
        "name": "Gaming",
        "icon": "🎮",
        "color": "#9C27B0",
        "gradient": ["#9C27B0", "#7B1FA2"],
        "category": "entertainment"
    },
    "shopping": {
        "name": "Shopping",
        "icon": "🛒",
        "color": "#E91E63",
        "gradient": ["#E91E63", "#C2185B"],
        "category": "personal"
    },
    "finance": {
        "name": "Finance",
        "icon": "💰",
        "color": "#4CAF50",
        "gradient": ["#4CAF50", "#2E7D32"],
        "category": "professional"
    },
    "social": {
        "name": "Social Media",
        "icon": "📱",
        "color": "#00BCD4",
        "gradient": ["#00BCD4", "#0097A7"],
        "category": "social"
    },
    "email": {
        "name": "Email",
        "icon": "📧",
        "color": "#F44336",
        "gradient": ["#F44336", "#D32F2F"],
        "category": "productivity"
    },
    "research": {
        "name": "Research",
        "icon": "📚",
        "color": "#673AB7",
        "gradient": ["#673AB7", "#512DA8"],
        "category": "educational"
    },
    "school": {
        "name": "School",
        "icon": "🎓",
        "color": "#3F51B5",
        "gradient": ["#3F51B5", "#303F9F"],
        "category": "educational"
    },
    "client_a": {
        "name": "Client A",
        "icon": "🤝",
        "color": "#009688",
        "gradient": ["#009688", "#00796B"],
        "category": "business"
    },
    "client_b": {
        "name": "Client B",
        "icon": "👔",
        "color": "#795548",
        "gradient": ["#795548", "#5D4037"],
        "category": "business"
    },
    "freelance": {
        "name": "Freelance",
        "icon": "💼",
        "color": "#FF5722",
        "gradient": ["#FF5722", "#E64A19"],
        "category": "professional"
    },
    "creative": {
        "name": "Creative",
        "icon": "🎨",
        "color": "#E91E63",
        "gradient": ["#E91E63", "#AD1457"],
        "category": "creative"
    },
    "music": {
        "name": "Music",
        "icon": "🎵",
        "color": "#9C27B0",
        "gradient": ["#9C27B0", "#6A1B9A"],
        "category": "entertainment"
    },
    "video": {
        "name": "Video",
        "icon": "🎬",
        "color": "#F44336",
        "gradient": ["#F44336", "#C62828"],
        "category": "entertainment"
    },
    "travel": {
        "name": "Travel",
        "icon": "✈️",
        "color": "#00BCD4",
        "gradient": ["#00BCD4", "#00838F"],
        "category": "personal"
    },
    "health": {
        "name": "Health",
        "icon": "💊",
        "color": "#4CAF50",
        "gradient": ["#4CAF50", "#2E7D32"],
        "category": "personal"
    },
    "fitness": {
        "name": "Fitness",
        "icon": "💪",
        "color": "#FF5722",
        "gradient": ["#FF5722", "#D84315"],
        "category": "personal"
    },
    "news": {
        "name": "News",
        "icon": "📰",
        "color": "#607D8B",
        "gradient": ["#607D8B", "#455A64"],
        "category": "information"
    },
    "sports": {
        "name": "Sports",
        "icon": "⚽",
        "color": "#8BC34A",
        "gradient": ["#8BC34A", "#689F38"],
        "category": "entertainment"
    },
    "food": {
        "name": "Food & Recipes",
        "icon": "🍕",
        "color": "#FF9800",
        "gradient": ["#FF9800", "#EF6C00"],
        "category": "personal"
    },
    "photography": {
        "name": "Photography",
        "icon": "📷",
        "color": "#9E9E9E",
        "gradient": ["#9E9E9E", "#616161"],
        "category": "creative"
    },
    "design": {
        "name": "Design",
        "icon": "🖌️",
        "color": "#E91E63",
        "gradient": ["#E91E63", "#C2185B"],
        "category": "creative"
    },
    "admin": {
        "name": "Admin",
        "icon": "⚙️",
        "color": "#607D8B",
        "gradient": ["#607D8B", "#455A64"],
        "category": "professional"
    },
    "testing": {
        "name": "Testing",
        "icon": "🧪",
        "color": "#673AB7",
        "gradient": ["#673AB7", "#512DA8"],
        "category": "professional"
    },
    "default": {
        "name": "Default",
        "icon": "🌐",
        "color": "#2196F3",
        "gradient": ["#2196F3", "#1976D2"],
        "category": "general"
    }
}

CATEGORIES = {
    "professional": "Professional & Business",
    "personal": "Personal Use",
    "educational": "Education & Learning",
    "entertainment": "Entertainment & Games",
    "creative": "Creative & Design",
    "business": "Client & Business",
    "productivity": "Productivity & Tools",
    "social": "Social Media",
    "information": "News & Information",
    "general": "General Purpose"
}

def get_template(template_id):
    """Get a specific template by ID"""
    return ICON_TEMPLATES.get(template_id, ICON_TEMPLATES["default"])

def get_templates_by_category(category):
    """Get all templates in a specific category"""
    return {k: v for k, v in ICON_TEMPLATES.items() if v["category"] == category}

def get_all_templates():
    """Get all available templates"""
    return ICON_TEMPLATES

def get_all_categories():
    """Get all template categories"""
    return CATEGORIES

def search_templates(query):
    """Search templates by name or category"""
    query = query.lower()
    return {
        k: v for k, v in ICON_TEMPLATES.items()
        if query in v["name"].lower() or query in v["category"].lower()
    }

def create_custom_template(name, icon, color, category="general", gradient=None):
    """Create a custom template"""
    if gradient is None:
        gradient = [color, color]

    return {
        "name": name,
        "icon": icon,
        "color": color,
        "gradient": gradient,
        "category": category
    }


# Example usage
if __name__ == "__main__":
    print("Available Icon Templates:")
    print("=" * 50)

    for category_id, category_name in CATEGORIES.items():
        templates = get_templates_by_category(category_id)
        if templates:
            print(f"\n{category_name}:")
            for template_id, template in templates.items():
                print(f"  {template['icon']} {template['name']} - {template['color']}")

    print("\n" + "=" * 50)
    print(f"Total templates: {len(ICON_TEMPLATES)}")
