import re


class Generator():
    document_setup = \
"""
%-------------------------
% Resume in Latex
% Author : Ajay Sarjoo
% License : MIT
%------------------------

\\documentclass[letterpaper, 10pt]{article}

\\usepackage{latexsym}
\\usepackage[empty]{fullpage}
\\usepackage{titlesec}
\\usepackage{marvosym}
\\usepackage[usenames,dvipsnames]{color}
\\usepackage{verbatim}
\\usepackage{enumitem}
\\usepackage[hidelinks]{hyperref}
\\usepackage{fancyhdr}
\\usepackage{fontspec}% !TEX parameter = % !TEX TS-program = lualatex
\\usepackage{fontawesome}


\\pagestyle{fancy}
\\fancyhf{} % clear all header and footer fields
\\fancyfoot{}
\\renewcommand{\\headrulewidth}{0pt}
\\renewcommand{\\footrulewidth}{0pt}

% Adjust margins
% ------------------------------------------------
% \\addtolength{\\oddsidemargin}{-0.5in}
% \\addtolength{\\evensidemargin}{-0.5in}
% \\addtolength{\\textwidth}{1in}
% \\addtolength{\\topmargin}{-.5in}
% \\addtolength{\\textheight}{1.0in}
% ------------------------------------------------
\\addtolength{\\oddsidemargin}{-.75in}
\\addtolength{\\evensidemargin}{-0.5in}
\\addtolength{\\textwidth}{1.45in}
\\addtolength{\\topmargin}{-.6in}
\\addtolength{\\textheight}{1.0in}

\\urlstyle{same}

\\raggedbottom
\\raggedright
\\setlength{\\tabcolsep}{0in}

% Sections formatting
\\titleformat{\\section}{
\\vspace{-6pt}\\scshape\\raggedright\\large
}{}{0em}{}[\\color{black}\\titlerule \\vspace{-5pt}]

%-------------------------
% Custom commands
\\newcommand{\\resumeItem}[2]{
	\\item\\small{
		\\textbf{#1}{#2 \\vspace{-3pt}}
	}
}
\\newcommand{\\resumeProjectItem}[2]{
	\\item\\small{
		\\textbf{#1}{#2 \\vspace{-2pt}}
	}
}

\\newcommand{\\resumeSubheadingEducation}[4]{
	\\vspace{-1pt}\\item[\\label{}]
		\\begin{tabular*}{0.97\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}
		\\textbf{#1} & #2 \\\\
		\\textit{\\small#3} & \\textit{\\small #4} \\\\
		\\end{tabular*}\\vspace{0pt}
}

\\newcommand{\\resumeSubheading}[4]{
	\\vspace{-1pt}\\item[\\label{}]
		\\begin{tabular*}{0.97\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}
		\\textbf{#1} & #2 \\\\
		\\textit{\\small#3} & \\textit{\\small #4} \\\\
		\\end{tabular*}\\vspace{-5pt}
}

\\newcommand{\\resumeSubheadingProject}[4]{
	\\vspace{-1pt}\\item[\\label{}]
		\\begin{tabular*}{0.97\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}
		{#1} & #2 \\\\
		\\end{tabular*}\\vspace{-6pt}
}

\\newcommand{\\resumeSubItem}[2]{\\resumeProjectItem{#1}{#2}\\vspace{-4pt}}

\\renewcommand{\\labelitemii}{$\\circ$}

\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=* \\label{}]}
\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}
\\newcommand{\\resumeItemListStart}{\\begin{itemize}\\vspace{2pt}}
\\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}

%-------------------------------------------
%%%%%%  CV STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%\n
"""

    start_doc = "\n\\begin{document}\n"
    end_doc = "\n\\end{document}"

    def __init__(self, resume_dict, args):
        self.resume_dict = resume_dict
        self.doc = str()
        self.args = args



    def build(self):
        self.doc += self.document_setup

        self.doc += self.start_doc

        # Build the header
        self.doc += self.generate_header()

        # Build the education
        self.doc += self.generate_education()

        # Build the experience
        if not self.args.no_experience:
            self.doc += self.generate_exp()

        # Build the projects
        if not self.args.no_projects:
            self.doc += self.generate_projects()

        # Build the extracurriculars
        if not self.args.no_extracurriculars:
            self.doc += self.generate_extracurriculars()

        # Build the skills section
        self.doc += self.generate_skills()

        # Finish
        self.doc += self.end_doc


    def generate_header(self):
        section = ""
        section += "\n%----------HEADING-----------------\n"
        section += "\\begin{center}\n" \
                  "\t\\textbf{\\Huge " + self.resume_dict['header']['name'] + "} \\\\[.1in]\n"

        if not self.args.no_phone:
            section += "\t{\\faMobile}{ " + self.resume_dict['header']['phone'] + "} | "

        section += "{\\faEnvelope}{\\href{mailto:" + self.resume_dict['header']['email'] + "}{ " + self.resume_dict['header']['email'] + "}} | "

        if not self.args.no_website:
            section += "{\\faLaptop}{\\href{" + self.resume_dict['header']['website'] + "}{ " + self.resume_dict['header']['website'][self.resume_dict['header']['website'].index("//") + 2:] + "}} | "

        section += "{\\faLinkedinSquare}{\\href{" + self.resume_dict['header']['linkedin'] + "}{ " + self.resume_dict['header']['linkedin'][self.resume_dict['header']['linkedin'].index("/in/") + 4:len(self.resume_dict['header']['linkedin']) - 1] + "}}"

        if not self.args.no_github:
            section += " | {\\faGithub}{\\href{" + self.resume_dict['header']['github'] + "}{ " + self.resume_dict['header']['github'][self.resume_dict['header']['github'].index(".com/") + 5:] + "}} "

        section += "\n\\end{center}\n"

        return section

    def generate_education(self):
        section = ""
        section += "\n%-----------EDUCATION-----------------\n"
        if not self.args.no_gpa:
            section += "\\section{Education}\n \
                    \\resumeSubHeadingListStart\n \
                        \\resumeSubheadingEducation\n \
                            {" + self.resume_dict['education']['university'] + "}{" + self.resume_dict['education']['location'] + "}\n \
                            {" + self.resume_dict['education']['degree'] + ", GPA: " + self.resume_dict['education']['gpa_honors'] + "}{" + self.resume_dict['education']['attended_range'] + "} \\\\ \n \
                            {" + ((self.resume_dict['education']['courses'].replace("&", "\&")) if not self.args.no_coursework else "") + "} \\\\ \n \
                    \\resumeSubHeadingListEnd\n"
        else:
            section += "\\section{Education}\n \
                                \\resumeSubHeadingListStart\n \
                                    \\resumeSubheadingEducation\n \
                                        {" + self.resume_dict['education']['university'] + "}{" + \
                       self.resume_dict['education']['location'] + "}\n \
                                        {" + self.resume_dict['education']['degree'] + "}{" + self.resume_dict['education'][
                           'attended_range'] + "} \\\\ \n \
                                        {" + ((self.resume_dict['education']['courses'].replace("&",
                                                                                                "\&")) if not self.args.no_coursework else "") + "} \\\\ \n \
                                \\resumeSubHeadingListEnd\n"

        return section

    def generate_exp(self):
        section = ""

        section += "\n%-----------EXPERIENCE-----------------\n \
                        \\section{Experience}\n \
                            \\resumeSubHeadingListStart\n"

        for exp in self.resume_dict['experience']:
            section += "\t\t\t\t\t\t\t\t\\resumeSubheading\n" \
                            "\t\t\t\t\t\t\t\t\t{" + exp['position'] + "}{" + exp['duration'] + "}\n" \
                            "\t\t\t\t\t\t\t\t\t{" + exp['company'] + "}{" + exp['location'] + "}\n"
            if len(exp['details']) > 0:
                section += "\t\t\t\t\t\t\t\t\t\t\\resumeItemListStart\n"

                for detail in exp['details']:
                    section += "\t\t\t\t\t\t\t\t\t\t\t\\resumeItem{}{" + detail.replace("%", "\%").replace("&", "\&") + "}\n"

                section += "\t\t\t\t\t\t\t\t\t\t\\resumeItemListEnd\n"

        section += "\t\t\t\t\t\t\t\\resumeSubHeadingListEnd\n"

        return section

    def generate_projects(self):
        section = ""

        section += "\n%-----------PROJECTS-----------------\n \
                                \\section{Projects}\n \
                                    \\resumeSubHeadingListStart\n"

        for project in self.resume_dict['projects']:
            section += "\t\t\t\t\t\t\t\t\\resumeSubheadingProject\n" \
                            "\t\t\t\t\t\t\t\t\t{\\textbf{" + project['name'] + "} \\textit{- " + project['languages'] + "}}{" + (project['duration'] if not self.args.no_project_dates else "") + "}\n" \
                            "\t\t\t\t\t\t\t\t\t{}{}\n"
            if len(project['details']) > 0:
                section += "\t\t\t\t\t\t\t\t\t\t\\resumeItemListStart\n"

                for detail in project['details']:
                    section += "\t\t\t\t\t\t\t\t\t\t\t\\resumeItem{}{" + detail.replace("%", "\%").replace("&", "\&") + "}\n"

                section += "\t\t\t\t\t\t\t\t\t\t\\resumeItemListEnd\n"

        section += "\t\t\t\t\t\t\t\\resumeSubHeadingListEnd\n"

        return section

    def generate_extracurriculars(self):
        section = ""

        section += "\n%-----------EXTRACURRICULARS-----------------\n \
                                \\section{Extracurriculars}\n \
                                    \\resumeSubHeadingListStart\n"

        for exp in self.resume_dict['extracurriculars']:
            section += "\t\t\t\t\t\t\t\t\\resumeSubheading\n" \
                            "\t\t\t\t\t\t\t\t\t{" + exp['position'] + "}{" + exp['duration'] + "}\n" \
                            "\t\t\t\t\t\t\t\t\t{" + exp['company'] + "}{" + exp['location'] + "}\n"
            if len(exp['details']) > 0:
                section += "\t\t\t\t\t\t\t\t\t\t\\resumeItemListStart\n"

                for detail in exp['details']:
                    section += "\t\t\t\t\t\t\t\t\t\t\t\\resumeItem{}{" + detail.replace("%", "\%").replace("&", "\&") + "}\n"

                section += "\t\t\t\t\t\t\t\t\t\t\\resumeItemListEnd\n"

        section += "\t\t\t\t\t\t\t\\resumeSubHeadingListEnd\n"

        return section

    def generate_skills(self):
        section = ""

        section += "\n%-----------SKILLS-----------------\n \
                \\section{Skills}\n \
                    \\resumeSubHeadingListStart\n"

        section += "\t\t\t\t\t\t\\itemsep-0.3em\n \
                        \\item[]{\n \
                                \\textbf{Languages}{: " + ", ".join(self.resume_dict['skills']['languages']) + "}\n \
                                \\noindent\\hbox to 0.225 \\textwidth{}\n \
                                \\textbf{Web Development}{: " + ", ".join(self.resume_dict['skills']['web_dev']) + "}\n \
                        }\n \
                    \t\\itemsep-0.3em\n \
                        \\item[]{\n \
                            \\textbf{Data}{: " + ", ".join(self.resume_dict['skills']['data']) + "}\n \
                                \\noindent\\hbox to 0.05 \\textwidth{}\n \
                                \\textbf{Tools and Technologies}{: " + ", ".join(self.resume_dict['skills']['tools_and_technologies']) + "}\n \
                        }\n \
                    \t\\itemsep-0.3em\n \
                        \item[]{\n \
                            \\textbf{Frameworks}{: " + ", ".join(self.resume_dict['skills']['frameworks']) + "}\n \
                            \\noindent\\hbox to 0.12 \\textwidth{}\n \
                                \\textbf{Software}{: " + ", ".join(self.resume_dict['skills']['software']) + "}\n \
                        }\n \
                "

        section += "\t\\resumeSubHeadingListEnd\n"

        return section