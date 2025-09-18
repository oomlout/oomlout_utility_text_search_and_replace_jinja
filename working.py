import oom_markdown
import os
import argparse
import robo

#process
#  locations set in working_parts.ods 
#  export to working_parts.csv
#  put components on the right side of the board
#  run this script

def main(**kwargs):
    file_template = kwargs.get('file_template', 'template\\test\working_inkscape.svg')
    file_output = kwargs.get('file_output', 'output\\test\\working.svg')
    file_source = kwargs.get('file_source', 'parts\\test')
    directory_single = kwargs.get('directory_single', '')
    directory_iterative = kwargs.get('directory_iterative', '')
    convert_pdf = kwargs.get('convert_pdf', True)


    #print utility name
    print("oomlout_utility_text_search_and_replace_jinja")
    #print parameters
    print(f"file_template: {file_template}")
    print(f"file_output: {file_output}")
    print(f"file_source: {file_source}")
    print(f"directory_single: {directory_single}")
    print(f"directory_iterative: {directory_iterative}")
    print(f"convert_pdf: {convert_pdf}")


    #load up files to run
    jobs = []
    job = {}
    if file_source != '':        
        if os.path.isdir(file_source):
            if not file_source.endswith('\\'):
                file_source += '\\'
            file_source += 'working.yaml'
        job['file_source'] = file_source
        job['file_template'] = file_template
        job['file_output'] = file_output
        jobs.append(job)
    elif directory_single != '':
        if not directory_single.endswith('\\'):
            directory_single += '\\'
        file_source = directory_single + 'working.yaml'
        if file_output != "":
            file_output = directory_single + 'working.svg'            
        else:
            file_output = directory_single + '\\' + file_output
        job['file_source'] = file_source
        job['file_template'] = file_template
        job['file_output'] = file_output
        jobs.append(job)
    elif directory_iterative != '':
        if not directory_iterative.endswith('\\'):
            directory_iterative += '\\'
        #get directory list for directory_iterative
        directories = os.listdir(directory_iterative)
        for directory in directories:
            dir_path = os.path.join(directory_iterative, directory)
            if os.path.isdir(dir_path):
                file_source = dir_path + '\\working.yaml'
                file_output = dir_path + '\\working.svg'
                job = {}
                job['file_source'] = file_source
                job['file_template'] = file_template
                job['file_output'] = file_output
                jobs.append(job)


    for job in jobs:
        kwargs.update(job)
        file_template = job.get('file_template', 'template\\test\working_inkscape.svg')
        file_output = job.get('file_output', 'output\\test\\working.svg')
        file_source = job.get('file_source', 'parts\\test')

        deets = {}
        deets["file_template"] = file_template
        deets["file_output"] = file_output
        deets["file_source"] = file_source
        robo.robo_text_jinja_template(**deets)
        if convert_pdf:
            deets = {}
            deets["file_input"] = file_output
            robo.robo_convert_svg_to_pdf(**deets)  


def make_readme(**kwargs):
    os.system("generate_resolution.bat")
    oom_markdown.generate_readme_project(**kwargs)
    #oom_markdown.generate_readme_teardown(**kwargs)


if __name__ == '__main__':
    
    # parse arguments
    argparser = argparse.ArgumentParser(description='project description')
    #--file_input -fi
    argparser.add_argument('--file_template', '-fi', type=str, default='template\\test\working_inkscape.svg', help='Inpur file name.')    
    argparser.add_argument('--file_output', '-fo', type=str, default='working_test.svg', help='Output file name.')
    argparser.add_argument('--file_source', '-fs', type=str, default='', help='Source yaml file, if directory provided working.yaml is added.')
    #directory_single
    argparser.add_argument('--directory_single', '-ds', type=str, default="parts\\test", help='A single directory to run on.')
    #directory_iterative
    argparser.add_argument('--directory_iterative', '-di', type=str, default="parts", help='Directory to run iterative on.')
    argparser.add_argument('--convert_pdf', '-cpdf', type=bool, default=True, help='Convert output file to pdf (bool).')
    args = argparser.parse_args()
    kwargs = {}
    # update kwargs with args
    kwargs.update(vars(args))
    main(**kwargs)