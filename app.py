import csv
import os
from datetime import datetime
from shiny import App, Inputs, Outputs, Session, reactive, render, ui

# 1. Define the User Interface (UI)
app_ui = ui.page_fluid(
    ui.h2("Data Collection Survey"),
    ui.p("Please complete the following questionnaire. All responses are confidential."),
    ui.hr(),

    # Gender Selection
    ui.input_radio_buttons(
        "gender",
        "Gender",
        {"male": "Male", "female": "Female", "other": "Other"}
    ),

    # Year of Birth
    ui.input_numeric(
        "yob",
        "Year of birth",
        value=2000,
        min=1900,
        max=2026
    ),

    # Main Activity Dropdown
    ui.input_select(
        "activity",
        "What is your main activity?",
        {
            "paid_work": "Paid work",
            "education": "Education",
            "unemployed_looking": "Unemployed, looking for job",
            "unemployed_not_looking": "Unemployed, not looking for job",
            "sick_disabled": "Permanently sick or disabled",
            "retired": "Retired",
            "service": "Community or military service",
            "housework": "Housework, looking after children, others",
            "other": "Other"
        }
    ),

    # Internet Usage
    ui.input_radio_buttons(
        "internet",
        "How often do you use the internet?",
        {
            "never": "Never",
            "occasionally": "Only occasionally",
            "few_times": "A few times a week",
            "most_days": "Most days",
            "every_day": "Every day"
        }
    ),

    ui.hr(),
    ui.h4("Artificial Intelligence Section"),

    # AI Confidence Slider
    ui.input_slider(
        "ai_confidence",
        "On a scale from 1-10 (10 being the highest), how confident are you on AI? (1 = Not confident at all, 10 = Totally confident)",
        min=1, max=10, value=5, step=1
    ),

    # AI Usage Reason Text Area
    ui.input_text_area(
        "ai_reason",
        "Why do you use artificial intelligence? Describe in a few lines why you use it.",
        width="100%",
        rows=4
    ),

    # AI Problems Boolean/Radio
    ui.input_radio_buttons(
        "ai_problems",
        "Do you think that artificial intelligence will cause problems in the future?",
        {"yes": "Yes", "no": "No"}
    ),

    ui.hr(),

    # Submit Button
    ui.input_action_button("submit", "Submit Survey", class_="btn-primary"),

    # Text output to show a confirmation message upon submission
    ui.output_text("submission_message")
)


# 2. Define the Server Logic
def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.text
    @reactive.event(input.submit)  # Triggers only when the submit button is clicked
    def submission_message():
        # Define the file path for saving data
        csv_filename = "survey_data.csv"

        # Check if the file already exists to determine if we need to write headers
        file_exists = os.path.isfile(csv_filename)

        # Gather all current inputs into a dictionary
        row_data = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Gender": input.gender(),
            "Year_of_Birth": input.yob(),
            "Main_Activity": input.activity(),
            "Internet_Usage": input.internet(),
            "AI_Confidence": input.ai_confidence(),
            "AI_Reason": input.ai_reason(),  # The csv module automatically handles text with commas/newlines here
            "AI_Problems": input.ai_problems()
        }

        # Define the column headers based on our dictionary keys
        fieldnames = list(row_data.keys())

        try:
            # Open the CSV file in 'append' mode ('a')
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                # Write the header row only if the file is being created for the first time
                if not file_exists:
                    writer.writeheader()

                # Write the user's data
                writer.writerow(row_data)

            return "Thank you! Your survey responses have been successfully saved to survey_data.csv."

        except Exception as e:
            # Provide an error message if something goes wrong (e.g., file permission issues)
            return f"An error occurred while saving your data: {e}"


# 3. Create and Run the Application
app = App(app_ui, server)