// Icon Template Browser for Chrome Extension
// Simplified version of icon_templates.py for use in extensions

const TEMPLATE_CATEGORIES = {
  professional: "Professional",
  personal: "Personal",
  entertainment: "Entertainment",
  creative: "Creative",
  business: "Business",
  educational: "Educational",
  social: "Social",
  productivity: "Productivity",
  finance: "Finance",
  all: "All Categories"
};

const ICON_TEMPLATES = {
  work: { name: "Work", icon: "💼", color: "#2196F3", category: "professional" },
  personal: { name: "Personal", icon: "🏠", color: "#4CAF50", category: "personal" },
  development: { name: "Development", icon: "💻", color: "#FF9800", category: "professional" },
  gaming: { name: "Gaming", icon: "🎮", color: "#9C27B0", category: "entertainment" },
  shopping: { name: "Shopping", icon: "🛒", color: "#E91E63", category: "personal" },
  finance: { name: "Finance", icon: "💰", color: "#4CAF50", category: "finance" },
  social: { name: "Social Media", icon: "📱", color: "#00BCD4", category: "social" },
  email: { name: "Email", icon: "📧", color: "#F44336", category: "productivity" },
  research: { name: "Research", icon: "📚", color: "#673AB7", category: "educational" },
  school: { name: "School", icon: "🎓", color: "#3F51B5", category: "educational" },
  creative: { name: "Creative", icon: "🎨", color: "#E91E63", category: "creative" },
  music: { name: "Music", icon: "🎵", color: "#9C27B0", category: "entertainment" },
  travel: { name: "Travel", icon: "✈️", color: "#00BCD4", category: "personal" },
  health: { name: "Health", icon: "💊", color: "#4CAF50", category: "personal" },
  fitness: { name: "Fitness", icon: "💪", color: "#FF5722", category: "personal" },
  news: { name: "News", icon: "📰", color: "#607D8B", category: "productivity" },
  sports: { name: "Sports", icon: "⚽", color: "#8BC34A", category: "entertainment" },
  food: { name: "Food", icon: "🍕", color: "#FF9800", category: "personal" },
  photography: { name: "Photography", icon: "📷", color: "#9E9E9E", category: "creative" },
  design: { name: "Design", icon: "🖌️", color: "#E91E63", category: "creative" },
  admin: { name: "Admin", icon: "⚙️", color: "#607D8B", category: "professional" },
  testing: { name: "Testing", icon: "🧪", color: "#673AB7", category: "professional" },
  coding: { name: "Coding", icon: "👨‍💻", color: "#00ACC1", category: "professional" },
  meetings: { name: "Meetings", icon: "📞", color: "#5C6BC0", category: "professional" },
  project: { name: "Project", icon: "📋", color: "#26A69A", category: "professional" },
  marketing: { name: "Marketing", icon: "📈", color: "#EC407A", category: "business" },
  sales: { name: "Sales", icon: "💵", color: "#66BB6A", category: "business" },
  streaming: { name: "Streaming", icon: "📺", color: "#EF5350", category: "entertainment" },
  podcast: { name: "Podcasts", icon: "🎙️", color: "#AB47BC", category: "entertainment" },
  books: { name: "Books", icon: "📖", color: "#8D6E63", category: "entertainment" }
};

function getTemplatesByCategory(category) {
  if (category === 'all') return ICON_TEMPLATES;

  return Object.fromEntries(
    Object.entries(ICON_TEMPLATES).filter(([_, template]) => template.category === category)
  );
}

function searchTemplates(query) {
  const lowerQuery = query.toLowerCase();
  return Object.fromEntries(
    Object.entries(ICON_TEMPLATES).filter(([_, template]) =>
      template.name.toLowerCase().includes(lowerQuery) ||
      template.category.toLowerCase().includes(lowerQuery)
    )
  );
}

function getTemplate(id) {
  return ICON_TEMPLATES[id] || null;
}

function getAllCategories() {
  return TEMPLATE_CATEGORIES;
}

// Make available globally
if (typeof window !== 'undefined') {
  window.TemplateLibrary = {
    TEMPLATE_CATEGORIES,
    ICON_TEMPLATES,
    getTemplatesByCategory,
    searchTemplates,
    getTemplate,
    getAllCategories
  };
}
