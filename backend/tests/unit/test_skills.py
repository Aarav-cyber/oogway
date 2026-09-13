import pytest
from app.agent.router import AgentRouter, AgentSkillType
from app.agent.skills.artifact import ArtifactSkill


def test_agent_router_intent_matching():
    assert AgentRouter.route_request("How do I improve retention?") == AgentSkillType.GROUNDED_QA
    assert AgentRouter.route_request("Write me a Ship 30 for 30 essay on product management") == AgentSkillType.SHIP30
    assert AgentRouter.route_request("Generate HTML page for this summary") == AgentSkillType.ARTIFACT


def test_artifact_skill_html_sanitization():
    unsafe_html = "<div class='content'><h1>Header</h1><script>alert('xss')</script><iframe src='http://evil.com'></iframe><p>Safe paragraph</p></div>"
    clean_html = ArtifactSkill.sanitize_html(unsafe_html)
    assert "<script>" not in clean_html
    assert "<iframe" not in clean_html
    assert "<h1>Header</h1>" in clean_html
    assert "<p>Safe paragraph</p>" in clean_html
