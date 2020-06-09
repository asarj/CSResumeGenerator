import re
from pprint import pprint


class TxtParser():
    def __init__(self, path_to_resume_txt):
        with open(file=path_to_resume_txt) as f:
            self.txt = f.read()

        self.sections = re.split(r"\n\n\n", self.txt)
        if (len(self.sections) != 6):
            raise Exception("Error occurred during initial scan, check your number of sections")

    def parse(self):
        basic_data = self.parse_basics(self.sections[0])
        education_data = self.parse_education(self.sections[1])
        experience_data = self.parse_experience(self.sections[2])
        project_data = self.parse_projects(self.sections[3])
        extras_data = self.parse_extras(self.sections[4])
        skills_data = self.parse_skills(self.sections[5])

        resume_dict = {
            **basic_data,
            **education_data,
            **experience_data,
            **project_data,
            **extras_data,
            **skills_data
        }

        return resume_dict

    def parse_basics(self, section: str) -> dict:
        data = {}
        parts = section.split("\n")
        if (parts[1] != 'BASICS'):
            raise Exception("Error occurred during basic info parsing, please check your BASICS section: section not found in proper position")
        data['name'] = parts[3]
        data['phone'] = parts[4]
        data['email'] = parts[5]
        data['website'] = parts[6]
        data['linkedin'] = parts[7]
        data['github'] = parts[8]

        section_data = {}
        section_data["header"] = data
        return section_data

    def parse_education(self, section: str) -> dict:
        data = {}
        parts = section.split("\n")
        if (parts[1] != 'EDUCATION'):
            raise Exception("Error occurred during basic info parsing, please check your EDUCATION section: section not found in proper position")
        data['university'], data['location'] = tuple(parts[3].split(" -- "))
        data['attended_range'] = parts[4].replace("* ", "")
        data['degree'] = parts[5].replace("* ", "")
        data['gpa_honors'] = parts[6].replace("* ", "").replace("Cumulative GPA: ", "")
        data['courses'] = parts[7].replace("* ", "")

        section_data = {}
        section_data["education"] = data
        return section_data

    def parse_experience(self, section: str) -> dict:
        data = []
        if section.split("\n")[1] != "EXPERIENCE":
            raise Exception("Error occurred during basic info parsing, please check your EXPERIENCE section: section not found in proper position")
        parts = re.split("\n\n", section[section.index("--------------------------------------\nEXPERIENCE\n---------------------------------------\n") + len("--------------------------------------\nEXPERIENCE\n---------------------------------------\n"):])
        for part in parts:
            header_marked = False
            exp_info = {}
            exp_info['details'] = []
            part = part.split("\n")
            for line in part:
                if "*" not in line:
                    if header_marked:
                        raise Exception("Error occurred during the parsing of the EXPERIENCE section, make sure your experiences are properly formatted")
                    else:
                        header_marked = True
                        header = line.split(r" -- ")
                        exp_info['position'] = header[0]
                        exp_info['company'] = header[1]
                        exp_info['location'] = header[2]
                        exp_info['duration'] = header[3]
                else:
                    exp_info['details'].append(line.replace("* ", ""))
            data.append(exp_info)

        section_data = {}
        section_data["experience"] = data
        return section_data

    def parse_projects(self, section: str) -> dict:
        data = []
        if section.split("\n")[1] != "PROJECTS":
            raise Exception("Error occurred during basic info parsing, please check your PROJECTS section: section not found in proper position")
        parts = re.split("\n\n", section[section.index("--------------------------------------\nPROJECTS\n---------------------------------------\n") + len("--------------------------------------\nPROJECTS\n---------------------------------------\n"):])
        for part in parts:
            header_marked = False
            exp_info = {}
            exp_info['details'] = []
            part = part.split("\n")
            for line in part:
                if "*" not in line:
                    if header_marked:
                        raise Exception("Error occurred during the parsing of the PROJECTS section, make sure your projects are properly formatted")
                    else:
                        header_marked = True
                        header = line.split(r" -- ")
                        exp_info['name'] = header[0]
                        exp_info['languages'] = header[1]
                        exp_info['duration'] = header[2]
                else:
                    exp_info['details'].append(line.replace("* ", ""))
            data.append(exp_info)

        section_data = {}
        section_data["projects"] = data
        return section_data

    def parse_extras(self, section: str) -> dict:
        data = []
        if section.split("\n")[1] != "EXTRACURRICULARS":
            raise Exception("Error occurred during basic info parsing, please check your EXTRACURRICULARS section: section not found in proper position")
        parts = re.split("\n\n", section[section.index("--------------------------------------\nEXTRACURRICULARS\n---------------------------------------\n") + len("--------------------------------------\nEXTRACURRICULARS\n---------------------------------------\n"):])
        for part in parts:
            header_marked = False
            exp_info = {}
            exp_info['details'] = []
            part = part.split("\n")
            for line in part:
                if "*" not in line:
                    if header_marked:
                        raise Exception("Error occurred during the parsing of the EXTRACURRICULARS section, make sure your experiences are properly formatted")
                    else:
                        header_marked = True
                        header = line.split(r" -- ")
                        exp_info['position'] = header[0]
                        exp_info['company'] = header[1]
                        exp_info['location'] = header[2]
                        exp_info['duration'] = header[3]
                else:
                    exp_info['details'].append(line.replace("* ", ""))
            data.append(exp_info)

        section_data = {}
        section_data["extracurriculars"] = data
        return section_data

    def parse_skills(self, section: str) -> dict:
        data = {}
        if section.split("\n")[1] != "LANGUAGES AND TECHNOLOGIES":
            raise Exception("Error occurred during basic info parsing, please check your SKILLS section: section not found in proper position")
        parts = re.split("\n\n", section[section.index(
            "--------------------------------------\nLANGUAGES AND TECHNOLOGIES\n---------------------------------------\n") + len(
            "--------------------------------------\nLANGUAGES AND TECHNOLOGIES\n---------------------------------------\n"):])
        data['languages'] = parts[0].replace("LANGUAGES\n", "").split(", ")
        data['web_dev'] = parts[1].replace("WEB DEVELOPMENT\n", "").split(", ")
        data['data'] = parts[2].replace("DATA\n", "").split(", ")
        data['tools_and_technologies'] = parts[3].replace("TOOLS AND TECHNOLOGIES\n", "").split(", ")
        data['frameworks'] = parts[4].replace("FRAMEWORKS\n", "").split(", ")
        data['software'] = parts[5].replace("SOFTWARE\n", "").split(", ")

        section_data = {}
        section_data["skills"] = data
        return section_data


if __name__ == "__main__":
    # Assume txt file parsed follows format (see README for details on format structure)
    pass