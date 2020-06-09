from txt_to_json import TxtParser
from tex_builder import Generator
from pprint import pprint
import argparse
import os
import sys
import json
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="resume_generator.py", description="Creates a CS-based resume")
    parser.add_argument("-i", "--input", type=str, required=True, help="The filename for generating the resume from")
    parser.add_argument("-o", "--output", type=str, required=True, help="The output destination for all generated files (MUST BE A DIRECTORY)")
    parser.add_argument("-resume-filename", type=str, required=False,
                        help="The name of the output file (DO NOT INCLUDE FILE EXTENSION)")
    parser.add_argument("--no-gpa", action="store_true", required=False,
                        help="Flag to remove GPA from the resume")
    parser.add_argument("--no-coursework", action="store_true", required=False,
                        help="Flag to remove coursework from the resume")
    parser.add_argument("--no-phone", action="store_true", required=False,
                        help="Flag to remove phone number from the resume")
    parser.add_argument("--no-website", action="store_true", required=False,
                        help="Flag to remove website link from the resume")
    parser.add_argument("--no-github", action="store_true", required=False,
                        help="Flag to remove Github link from the resume")
    parser.add_argument("--no-experience", action="store_true", required=False,
                        help="Flag to remove experience from the resume")
    parser.add_argument("--no-projects", action="store_true", required=False,
                        help="Flag to remove projects from the resume")
    parser.add_argument("--no-project-dates", action="store_true", required=False,
                        help="Flag to remove project durations from the resume")
    parser.add_argument("--no-extracurriculars", action="store_true", required=False,
                        help="Flag to remove extracurriculars from the resume")
    parser.add_argument("--keep-tex", action="store_true", required=False,
                        help="Flag to keep the .tex file from resume generation")
    args = parser.parse_args()
    # print(args)

    if not os.path.exists(args.input):
        print("Path to txt file does not exist, please correct the issue and try running the script again")
        sys.exit(1)

    p = TxtParser(path_to_resume_txt=args.input)
    resume_dict = p.parse()

    output_filename = args.resume_filename if args.resume_filename is not None else "resume"

    json_filename = args.output + output_filename + ".json"
    with open(json_filename, "w") as f:
        json.dump(resume_dict, f, indent=4)

    generator = Generator(resume_dict, args)
    generator.build()

    tex_filename = args.output + output_filename + ".tex"

    with open(tex_filename, 'w') as f:
        f.write(generator.doc)

    cmd = ['lualatex', tex_filename, '-output-directory=' + args.output]
    proc = subprocess.Popen(cmd)
    proc.communicate()
    retcode = proc.returncode
    if not retcode == 0:
        os.unlink(args.output + output_filename + '.pdf')
        raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))

    subprocess.call("mv " + output_filename + ".pdf" + " " + args.output + output_filename + ".pdf", shell=True)
    subprocess.call("mv " + output_filename + ".log" + " " + args.output + output_filename + ".log", shell=True)
    subprocess.call("mv " + output_filename + ".out" + " " + args.output + output_filename + ".out", shell=True)
    subprocess.call("mv " + output_filename + ".aux" + " " + args.output + output_filename + ".aux", shell=True)

    if not args.keep_tex:
        os.unlink(args.output + output_filename + ".tex")
        os.unlink(args.output + output_filename + ".log")
        os.unlink(args.output + output_filename + ".aux")
        os.unlink(args.output + output_filename + ".out")



    sys.exit(0)