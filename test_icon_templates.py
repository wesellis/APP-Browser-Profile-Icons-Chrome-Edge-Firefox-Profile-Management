"""
Unit tests for icon_templates module
"""

import pytest
from icon_templates import (
    get_template,
    get_templates_by_category,
    get_all_templates,
    get_all_categories,
    search_templates,
    create_custom_template,
    ICON_TEMPLATES,
    CATEGORIES
)


class TestIconTemplates:
    """Test icon template functionality"""

    def test_get_template_valid(self):
        """Test getting a valid template"""
        template = get_template("work")
        assert template is not None
        assert template["name"] == "Work"
        assert template["icon"] == "💼"
        assert template["color"] == "#2196F3"

    def test_get_template_invalid(self):
        """Test getting an invalid template returns default"""
        template = get_template("nonexistent")
        assert template is not None
        assert template["name"] == "Default"

    def test_get_all_templates(self):
        """Test getting all templates"""
        templates = get_all_templates()
        assert isinstance(templates, dict)
        assert len(templates) > 0
        assert "work" in templates
        assert "personal" in templates

    def test_get_all_categories(self):
        """Test getting all categories"""
        categories = get_all_categories()
        assert isinstance(categories, dict)
        assert len(categories) > 0
        assert "professional" in categories
        assert "personal" in categories

    def test_get_templates_by_category(self):
        """Test getting templates by category"""
        professional = get_templates_by_category("professional")
        assert isinstance(professional, dict)
        assert len(professional) > 0

        # All templates should be professional category
        for template in professional.values():
            assert template["category"] == "professional"

    def test_search_templates(self):
        """Test searching templates"""
        results = search_templates("work")
        assert isinstance(results, dict)
        assert len(results) > 0

        results = search_templates("professional")
        assert len(results) > 0

    def test_search_templates_case_insensitive(self):
        """Test search is case insensitive"""
        results_lower = search_templates("work")
        results_upper = search_templates("WORK")
        assert len(results_lower) == len(results_upper)

    def test_create_custom_template(self):
        """Test creating a custom template"""
        custom = create_custom_template(
            name="Custom",
            icon="🔧",
            color="#FF0000",
            category="custom"
        )

        assert custom["name"] == "Custom"
        assert custom["icon"] == "🔧"
        assert custom["color"] == "#FF0000"
        assert custom["category"] == "custom"
        assert isinstance(custom["gradient"], list)
        assert len(custom["gradient"]) == 2

    def test_create_custom_template_with_gradient(self):
        """Test creating custom template with gradient"""
        custom = create_custom_template(
            name="Custom",
            icon="🔧",
            color="#FF0000",
            category="custom",
            gradient=["#FF0000", "#00FF00"]
        )

        assert custom["gradient"] == ["#FF0000", "#00FF00"]

    def test_template_structure(self):
        """Test that all templates have required fields"""
        for template_id, template in ICON_TEMPLATES.items():
            assert "name" in template
            assert "icon" in template
            assert "color" in template
            assert "gradient" in template
            assert "category" in template

            # Validate gradient is a list of 2 colors
            assert isinstance(template["gradient"], list)
            assert len(template["gradient"]) == 2

    def test_category_validity(self):
        """Test that all template categories are valid"""
        for template in ICON_TEMPLATES.values():
            assert template["category"] in CATEGORIES

    def test_color_format(self):
        """Test that colors are in hex format"""
        for template in ICON_TEMPLATES.values():
            # Check main color
            assert template["color"].startswith("#")
            assert len(template["color"]) == 7

            # Check gradient colors
            for grad_color in template["gradient"]:
                assert grad_color.startswith("#")
                assert len(grad_color) == 7

    def test_icon_exists(self):
        """Test that all templates have an icon"""
        for template in ICON_TEMPLATES.items():
            assert template["icon"] != ""
            assert len(template["icon"]) > 0


class TestTemplateIntegration:
    """Integration tests for template system"""

    def test_get_work_templates(self):
        """Test getting work-related templates"""
        results = search_templates("work")
        assert len(results) > 0
        assert "work" in results

    def test_get_creative_category(self):
        """Test getting creative category templates"""
        creative = get_templates_by_category("creative")
        assert len(creative) > 0

        # Should include creative, design, etc
        template_names = [t["name"] for t in creative.values()]
        assert any("Creative" in name or "Design" in name or "Photography" in name
                  for name in template_names)

    def test_professional_templates_count(self):
        """Test that we have a good number of professional templates"""
        professional = get_templates_by_category("professional")
        assert len(professional) >= 3  # Should have at least work, dev, admin

    def test_default_template_exists(self):
        """Test that default template is always available"""
        default = get_template("default")
        assert default is not None
        assert default["name"] == "Default"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
