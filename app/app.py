import os
import sys

import gradio as gr

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.resume_parser import extract_text_from_pdf
from src.ats_score import calculate_ats_score
from src.readiness_score import calculate_readiness_score, readiness_status

from agents.resume_agent import analyze_resume
from agents.skill_gap_agent import identify_skill_gaps
from agents.roadmap_agent import generate_roadmap
from agents.project_agent import recommend_projects
from agents.interview_agent import generate_interview_questions
from agents.recruiter_agent import recruiter_decision
from agents.resources_agent import recommend_learning_resources


PINK = "#ec4899"


custom_css = """
:root {
    --body-background-fill: #ffeaf3;
    --background-fill-primary: transparent;
    --background-fill-secondary: rgba(255, 255, 255, 0.72);
    --block-background-fill: rgba(255, 255, 255, 0.74);
    --block-border-color: #ffc7dd;
    --border-color-primary: #ffc7dd;
    --body-text-color: #4a2536;
    --body-text-color-subdued: #7a6170;
    --input-background-fill: rgba(255, 255, 255, 0.88);
    --input-border-color: #ffd0e1;
    --button-primary-background-fill: #ec4899;
    --button-primary-text-color: white;
    --link-text-color: #db2777;
}

html,
body,
#root,
.gradio-container {
    min-height: 100vh;
    background:
        radial-gradient(circle at 12% 4%, rgba(255, 255, 255, 0.95), transparent 18rem),
        radial-gradient(circle at 76% 10%, rgba(255, 255, 255, 0.82), transparent 20rem),
        linear-gradient(135deg, #fff7fb 0%, #ffe8f2 45%, #ffddea 100%) !important;
    color: #4a2536 !important;
    font-family: Inter, "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 8px 20px 24px !important;
}

.main,
.wrap,
.contain {
    max-width: 100% !important;
}

.block,
.form,
.panel {
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}

.hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    min-height: 132px;
    padding: 28px 38px;
    margin: 0 0 28px;
    border: 1px solid #ffc7dd;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.72);
    box-shadow: 0 18px 50px rgba(236, 72, 153, 0.10);
}

.hero-left {
    display: flex;
    align-items: center;
    gap: 22px;
}

.bot-badge {
    display: grid;
    place-items: center;
    width: 58px;
    height: 58px;
    border-radius: 18px;
    background: linear-gradient(145deg, #ffe0ee, #fff8fb);
    box-shadow: inset 0 0 0 1px #ffc7dd, 0 10px 26px rgba(236, 72, 153, 0.15);
    font-size: 38px;
}

.hero h1 {
    margin: 0 0 8px;
    color: #db2777 !important;
    font-size: 34px !important;
    font-weight: 900 !important;
    line-height: 1.08 !important;
    letter-spacing: 0 !important;
}

.hero p {
    margin: 0;
    color: #5e3a4b !important;
    font-size: 16px !important;
}

.last-analysis {
    width: 158px;
    min-height: 78px;
    padding: 16px;
    border: 1px solid #ffd0e1;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.66);
    text-align: center;
    color: #4a2536;
    box-shadow: 0 12px 30px rgba(236, 72, 153, 0.08);
}

.last-analysis strong {
    display: block;
    margin-bottom: 10px;
    font-size: 14px;
    color: #4a2536;
}

.last-analysis span {
    color: #ec4899;
    font-size: 18px;
    font-weight: 800;
}

.left-panel {
    min-height: 690px;
    padding: 26px 20px;
    border: 1px solid #ffc7dd;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.74);
    box-shadow: 0 18px 45px rgba(236, 72, 153, 0.12);
}

.step-title {
    margin: 0 0 16px;
    color: #ec4899;
    font-size: 16px;
    font-weight: 900;
}

.privacy-note {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-top: 32px;
    padding: 16px;
    border: 1px solid #ffd0e1;
    border-radius: 9px;
    background: rgba(255, 247, 251, 0.86);
    color: #7a6170;
    text-align: center;
}

.privacy-note strong {
    color: #ec4899;
    font-weight: 700;
}

.metric-card {
    display: flex;
    align-items: center;
    gap: 18px;
    min-height: 136px;
    padding: 26px 22px;
    border: 1px solid #ffc7dd;
    border-radius: 13px;
    background: rgba(255, 255, 255, 0.76);
    box-shadow: 0 14px 36px rgba(236, 72, 153, 0.12);
}

.metric-output [data-testid="block-label"],
.metric-output [data-testid="status-tracker"],
.metric-output .label-wrap,
.metric-output .icon-button-wrapper,
.metric-output button[aria-label="Clear"],
.metric-output button[title="Clear"] {
    display: none !important;
}

.metric-icon,
.agent-icon {
    display: grid;
    place-items: center;
    width: 58px;
    height: 58px;
    flex: 0 0 58px;
    border-radius: 999px;
    background: #ffe0ee;
    color: #ec4899;
    font-size: 26px;
}

.metric-copy h3,
.agent-card h3 {
    margin: 0 0 12px;
    color: #4a2536;
    font-size: 15px;
    font-weight: 800;
}

.metric-value {
    margin-bottom: 10px;
    color: #ec4899;
    font-size: 24px;
    font-weight: 900;
}

.metric-copy p,
.agent-card p {
    margin: 0;
    color: #6e5a67;
    line-height: 1.55;
}

.agent-section {
    margin-top: 28px;
    padding: 28px 16px 18px;
    border: 1px solid #ffc7dd;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.75);
    box-shadow: 0 18px 45px rgba(236, 72, 153, 0.11);
}

.section-title {
    margin: 0 0 8px;
    color: #ec4899;
    font-size: 24px;
    font-weight: 900;
}

.section-subtitle {
    margin: 0 0 24px;
    color: #6e5a67;
}

.agent-card {
    min-height: 202px;
    padding: 18px;
    border: 1px solid #ffd0e1;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.80);
    box-shadow: 0 12px 26px rgba(236, 72, 153, 0.08);
}

.agent-card .block,
.agent-card .form,
.agent-card .panel {
    background: transparent !important;
    border: 0 !important;
    padding: 0 !important;
}

.agent-head {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
}

.agent-btn {
    display: block;
    margin-top: 18px;
    padding: 11px 14px;
    border: 1px solid #ffd0e1;
    border-radius: 8px;
    background: linear-gradient(180deg, #fff3f8, #ffe7f0);
    color: #ec4899;
    text-align: center;
    font-weight: 800;
}

.agent-action {
    width: 100%;
    margin-top: 18px !important;
    min-height: 42px !important;
    border: 1px solid #ffd0e1 !important;
    border-radius: 8px !important;
    background: linear-gradient(180deg, #fff3f8, #ffe7f0) !important;
    color: #ec4899 !important;
    font-weight: 800 !important;
    box-shadow: none !important;
}

.selected-agent {
    margin-top: 22px;
    padding: 18px;
    border: 1px solid #ffd0e1;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.80);
}

.selected-agent .markdown,
.selected-agent .prose,
.selected-agent p,
.selected-agent li,
.selected-agent strong,
.selected-agent h1,
.selected-agent h2,
.selected-agent h3 {
    color: #4a2536 !important;
}

.details-shell {
    margin-top: 22px;
}

.details-shell .block {
    background: rgba(255, 255, 255, 0.78) !important;
    border: 1px solid #ffd0e1 !important;
    border-radius: 12px !important;
    padding: 14px !important;
}

.details-shell .markdown,
.details-shell .prose,
.details-shell p,
.details-shell li,
.details-shell strong,
.details-shell h1,
.details-shell h2,
.details-shell h3 {
    color: #4a2536 !important;
}

.footer {
    position: relative;
    overflow: hidden;
    min-height: 108px;
    margin-top: 22px;
    padding: 30px 36px;
    border: 1px solid #ffc7dd;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.70);
    box-shadow: 0 18px 45px rgba(236, 72, 153, 0.10);
}

.footer strong {
    color: #ec4899;
    font-size: 18px;
}

.footer p {
    margin: 6px 0 0;
    color: #4a2536;
}

.mountain {
    position: absolute;
    right: 34px;
    bottom: 0;
    width: 430px;
    height: 78px;
    opacity: 0.72;
    background:
        linear-gradient(145deg, transparent 40%, #f9a8d4 41% 58%, transparent 59%) 170px 12px / 130px 66px no-repeat,
        linear-gradient(145deg, transparent 43%, #f472b6 44% 60%, transparent 61%) 245px 0 / 180px 86px no-repeat,
        linear-gradient(145deg, transparent 42%, #fbcfe8 43% 61%, transparent 62%) 40px 36px / 150px 52px no-repeat;
}

.run-btn {
    width: 100%;
    min-height: 52px !important;
    border: 0 !important;
    border-radius: 9px !important;
    background: linear-gradient(90deg, #fb7185, #ec4899) !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: 900 !important;
    box-shadow: 0 12px 24px rgba(236, 72, 153, 0.28) !important;
}

label {
    color: #ec4899 !important;
    font-weight: 800 !important;
}

textarea,
input,
.input,
.upload-container,
[data-testid="file-upload"] {
    border-color: #ffd0e1 !important;
    border-radius: 10px !important;
    background: rgba(255, 255, 255, 0.9) !important;
    color: #4a2536 !important;
}

textarea::placeholder,
input::placeholder {
    color: #9f8a96 !important;
    opacity: 1 !important;
}

@media (max-width: 900px) {
    .hero,
    .hero-left {
        align-items: flex-start;
        flex-direction: column;
    }

    .last-analysis {
        width: 100%;
    }

    .hero h1 {
        font-size: 28px !important;
    }

    .mountain {
        display: none;
    }
}
"""


def metric_card(icon, title, value, caption):
    return f"""
<div class="metric-card">
    <div class="metric-icon">{icon}</div>
    <div class="metric-copy">
        <h3>{title}</h3>
        <div class="metric-value">{value}</div>
        <p>{caption}</p>
    </div>
</div>
"""


def agent_card(icon, title, body, badge=""):
    badge_html = f'<span class="agent-btn" style="margin-left:auto; display:inline-block; padding:6px 12px;">{badge}</span>' if badge else ""
    return f"""
<div class="agent-card">
    <div class="agent-head">
        <div class="agent-icon">{icon}</div>
        <h3>{title}</h3>
        {badge_html}
    </div>
    <p>{body}</p>
</div>
"""


def show_agent_result(title, result):
    result = "" if result is None else str(result)
    if not result.strip() or result.strip() == "Waiting...":
        return f"## {title}\n\nRun Career Coach first to generate this section."
    return f"## {title}\n\n{result}"


def show_recruiter_result(result):
    return show_agent_result("Recruiter Agent", result)


def show_resources_result(result):
    return show_agent_result("Learning Resources", result)


def show_resume_result(result):
    return show_agent_result("Resume Analysis", result)


def show_skill_result(result):
    return show_agent_result("Skill Gap Analysis", result)


def show_roadmap_result(result):
    return show_agent_result("Career Roadmap", result)


def show_projects_result(result):
    return show_agent_result("Project Recommendations", result)


def show_interview_result(result):
    return show_agent_result("Interview Preparation", result)


def show_bonus_result(result):
    return show_agent_result("Bonus Insights", result)


def safe_agent_call(title, fn, *args):
    try:
        return fn(*args)
    except Exception as exc:
        return f"Could not generate {title} right now.\n\nError: {exc}"


def run_career_coach(resume_file, target_role):
    if resume_file is None:
        return (
            metric_card("&#128202;", "ATS Score", "--%", "Upload resume first"),
            metric_card("&#127942;", "Career Readiness", "--/100", "Waiting for analysis"),
            metric_card("&#128188;", "Shortlist Chance", "--", "Waiting for recruiter outlook"),
            metric_card("&#9889;", "Improvement Areas", "--", "Waiting for skill gaps"),
            "Upload resume first.",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
        )

    if not target_role.strip():
        return (
            metric_card("&#128202;", "ATS Score", "--%", "Enter target role first"),
            metric_card("&#127942;", "Career Readiness", "--/100", "Waiting for analysis"),
            metric_card("&#128188;", "Shortlist Chance", "--", "Waiting for recruiter outlook"),
            metric_card("&#9889;", "Improvement Areas", "--", "Waiting for skill gaps"),
            "Enter target role first.",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
            "Waiting...",
        )

    try:
        resume_text = extract_text_from_pdf(resume_file)
        ats_score = calculate_ats_score(resume_text, target_role)
        resume_words = resume_text.split()

        readiness_score = calculate_readiness_score(
            ats_score=ats_score,
            num_projects=5,
            num_skills=len(set(resume_words)),
        )
        readiness_label = readiness_status(readiness_score)
    except Exception as exc:
        error_message = f"Resume analysis failed.\n\nError: {exc}"
        return (
            metric_card("&#128202;", "ATS Score", "--%", "Analysis failed"),
            metric_card("&#127942;", "Career Readiness", "--/100", "Analysis failed"),
            metric_card("&#128188;", "Shortlist Chance", "--", "Analysis failed"),
            metric_card("&#9889;", "Improvement Areas", "--", "Analysis failed"),
            error_message,
            error_message,
            error_message,
            error_message,
            error_message,
            error_message,
            error_message,
            error_message,
            error_message,
            error_message,
            error_message,
            error_message,
            error_message,
            error_message,
            error_message,
        )

    recruiter_feedback = safe_agent_call(
        "recruiter feedback", recruiter_decision, resume_text, target_role, ats_score
    )
    resources = safe_agent_call(
        "learning resources", recommend_learning_resources, resume_text, target_role
    )
    resume_feedback = safe_agent_call(
        "resume analysis", analyze_resume, resume_text, target_role
    )
    skill_gaps = safe_agent_call(
        "skill gap analysis", identify_skill_gaps, resume_text, target_role
    )
    roadmap = safe_agent_call(
        "career roadmap", generate_roadmap, resume_text, target_role
    )
    projects = safe_agent_call(
        "project recommendations", recommend_projects, resume_text, target_role
    )
    interview_questions = safe_agent_call(
        "interview preparation", generate_interview_questions, resume_text, target_role
    )

    return (
        metric_card("&#128202;", "ATS Score", f"{ats_score}%", f"Resume match for {target_role}"),
        metric_card("&#127942;", "Career Readiness", f"{readiness_score}/100", readiness_label),
        metric_card("&#128188;", "Shortlist Chance", "Ready", "Recruiter outlook generated"),
        metric_card("&#9889;", "Improvement Areas", "Ready", "Skills to focus identified"),
        recruiter_feedback,
        resources,
        resume_feedback,
        skill_gaps,
        roadmap,
        projects,
        interview_questions,
        recruiter_feedback,
        resources,
        resume_feedback,
        skill_gaps,
        roadmap,
        projects,
        interview_questions,
        f"""
### Bonus Insights

Target role: **{target_role}**

- ATS score: **{ats_score}%**
- Career readiness: **{readiness_score}/100**
- Current status: **{readiness_label}**

Focus first on the skill gaps, then build one portfolio project that proves those skills.
""",
    )


app_theme = gr.themes.Soft(primary_hue="pink", secondary_hue="rose")


with gr.Blocks() as demo:
    gr.HTML(
        """
        <div class="hero">
            <div class="hero-left">
                <div class="bot-badge">&#129302;</div>
                <div>
                    <h1>Multi-Agent AI Career Coach &#10024;</h1>
                    <p>Your AI-powered career companion for analysis, guidance &amp; growth.</p>
                </div>
            </div>
            <div class="last-analysis">
                <strong>&#128338; Last Analysis</strong>
                <span>--</span>
            </div>
        </div>
        """
    )

    with gr.Row(equal_height=True):
        with gr.Column(scale=1, min_width=330):
            with gr.Group(elem_classes="left-panel"):
                gr.HTML('<div class="step-title">&#128228; 1. Upload Your Resume</div>')
                resume_input = gr.File(
                    label="Upload Resume PDF",
                    file_types=[".pdf"],
                )

                gr.HTML('<div class="step-title" style="margin-top:24px;">&#127919; 2. Enter Target Role</div>')
                role_input = gr.Textbox(
                    label="Target Role",
                    placeholder="e.g., AI/ML Engineer",
                )

                run_button = gr.Button(
                    "Run Career Coach",
                    elem_classes="run-btn",
                )

                gr.HTML(
                    """
                    <div class="privacy-note">
                        <span>&#128737;</span>
                        <div><strong>Your data is safe and private.</strong><br>We never store your resume.</div>
                    </div>
                    """
                )

        with gr.Column(scale=3):
            with gr.Row():
                ats_output = gr.HTML(
                    metric_card("&#128202;", "ATS Score", "--%", "Resume Match"),
                    elem_classes="metric-output",
                )
                readiness_output = gr.HTML(
                    metric_card("&#127942;", "Career Readiness", "--/100", "Overall Score"),
                    elem_classes="metric-output",
                )
                recruiter_summary_output = gr.HTML(
                    metric_card("&#128188;", "Shortlist Chance", "--", "Recruiter Outlook"),
                    elem_classes="metric-output",
                )
                gaps_summary_output = gr.HTML(
                    metric_card("&#9889;", "Improvement Areas", "--", "Skills to Focus"),
                    elem_classes="metric-output",
                )

            with gr.Group(elem_classes="agent-section"):
                gr.HTML(
                    """
                    <div>
                        <h2 class="section-title">&#129504; AI Agent Outputs</h2>
                        <p class="section-subtitle">Insights and recommendations from our specialized AI agents</p>
                    </div>
                    """
                )

                with gr.Row():
                    with gr.Column(elem_classes="agent-card"):
                        gr.HTML(agent_card("&#128100;", "Recruiter Agent", "Recruiter-style evaluation and shortlist recommendation", "New"))
                        recruiter_btn = gr.Button("View Details", elem_classes="agent-action")
                    with gr.Column(elem_classes="agent-card"):
                        gr.HTML(agent_card("&#128218;", "Learning Resources", "Courses, certifications, books and learning platforms"))
                        resources_btn = gr.Button("View Details", elem_classes="agent-action")
                    with gr.Column(elem_classes="agent-card"):
                        gr.HTML(agent_card("&#128196;", "Resume Analysis", "Strengths, weaknesses and improvement suggestions"))
                        resume_btn = gr.Button("View Details", elem_classes="agent-action")
                    with gr.Column(elem_classes="agent-card"):
                        gr.HTML(agent_card("&#9888;", "Skill Gap Analysis", "Missing skills and technologies you should learn"))
                        skill_btn = gr.Button("View Details", elem_classes="agent-action")

                with gr.Row():
                    with gr.Column(elem_classes="agent-card"):
                        gr.HTML(agent_card("&#128506;", "Career Roadmap", "Personalized 6-month step-by-step roadmap"))
                        roadmap_btn = gr.Button("View Details", elem_classes="agent-action")
                    with gr.Column(elem_classes="agent-card"):
                        gr.HTML(agent_card("&#128187;", "Project Recommendations", "Best projects to build your portfolio and skills"))
                        projects_btn = gr.Button("View Details", elem_classes="agent-action")
                    with gr.Column(elem_classes="agent-card"):
                        gr.HTML(agent_card("&#127908;", "Interview Preparation", "Technical, behavioral and project-based questions"))
                        interview_btn = gr.Button("View Details", elem_classes="agent-action")
                    with gr.Column(elem_classes="agent-card"):
                        gr.HTML(agent_card("&#11088;", "Bonus Insights", "Additional tips and career growth suggestions"))
                        bonus_btn = gr.Button("View Details", elem_classes="agent-action")

                selected_agent_output = gr.Markdown(
                    "## Select an Agent\n\nClick any View Details button after running the career coach.",
                    elem_classes="selected-agent",
                )

                with gr.Accordion("Detailed Agent Results", open=False, elem_classes="details-shell"):
                    with gr.Tabs():
                        with gr.Tab("Recruiter Agent"):
                            recruiter_output = gr.Markdown()

                        with gr.Tab("Learning Resources"):
                            resources_output = gr.Markdown()

                        with gr.Tab("Resume Analysis"):
                            resume_output = gr.Markdown()

                        with gr.Tab("Skill Gap Analysis"):
                            skill_output = gr.Markdown()

                        with gr.Tab("Career Roadmap"):
                            roadmap_output = gr.Markdown()

                        with gr.Tab("Project Ideas"):
                            project_output = gr.Markdown()

                        with gr.Tab("Interview Prep"):
                            interview_output = gr.Markdown()

    recruiter_store = gr.Textbox(value="Waiting...", visible=False)
    resources_store = gr.Textbox(value="Waiting...", visible=False)
    resume_store = gr.Textbox(value="Waiting...", visible=False)
    skill_store = gr.Textbox(value="Waiting...", visible=False)
    roadmap_store = gr.Textbox(value="Waiting...", visible=False)
    projects_store = gr.Textbox(value="Waiting...", visible=False)
    interview_store = gr.Textbox(value="Waiting...", visible=False)
    bonus_store = gr.Textbox(value="Waiting...", visible=False)

    gr.HTML(
        """
        <div class="footer">
            <strong>&#10024; Your dream career is closer than you think.</strong>
            <p>Keep learning, keep building, and let AI guide your journey! &#128151;</p>
            <div class="mountain"></div>
        </div>
        """
    )

    run_button.click(
        fn=run_career_coach,
        inputs=[resume_input, role_input],
        outputs=[
            ats_output,
            readiness_output,
            recruiter_summary_output,
            gaps_summary_output,
            recruiter_output,
            resources_output,
            resume_output,
            skill_output,
            roadmap_output,
            project_output,
            interview_output,
            recruiter_store,
            resources_store,
            resume_store,
            skill_store,
            roadmap_store,
            projects_store,
            interview_store,
            bonus_store,
        ],
    )

    recruiter_btn.click(
        fn=show_recruiter_result,
        inputs=[recruiter_store],
        outputs=[selected_agent_output],
    )
    resources_btn.click(
        fn=show_resources_result,
        inputs=[resources_store],
        outputs=[selected_agent_output],
    )
    resume_btn.click(
        fn=show_resume_result,
        inputs=[resume_store],
        outputs=[selected_agent_output],
    )
    skill_btn.click(
        fn=show_skill_result,
        inputs=[skill_store],
        outputs=[selected_agent_output],
    )
    roadmap_btn.click(
        fn=show_roadmap_result,
        inputs=[roadmap_store],
        outputs=[selected_agent_output],
    )
    projects_btn.click(
        fn=show_projects_result,
        inputs=[projects_store],
        outputs=[selected_agent_output],
    )
    interview_btn.click(
        fn=show_interview_result,
        inputs=[interview_store],
        outputs=[selected_agent_output],
    )
    bonus_btn.click(
        fn=show_bonus_result,
        inputs=[bonus_store],
        outputs=[selected_agent_output],
    )


if __name__ == "__main__":
    demo.launch(css=custom_css, theme=app_theme)
