import os
import json


def get_input_data(json_file_name):
    with open(json_file_name, 'r') as input_file:
        data = json.load(input_file)
    return data


def render_jinja_template(directory, templates, input_data, output_file_name):
    from jinja2 import Environment, FileSystemLoader

    final_output = ""
    # Capture our current directory
    j2_env = Environment(loader=FileSystemLoader(directory),
                         trim_blocks=True)
    for temp in templates:
        render_resp = j2_env.get_template(temp).render(**input_data)
        final_output += render_resp

    with open(output_file_name, 'w') as h:
        h.write(final_output)

    return final_output


def get_j2files_from_dir(dir_name, file_type):
    j2_files = []
    directory_list = os.listdir(dir_name)
    if directory_list:
        for ele in directory_list:
            file_parts = ele.split(".")
            if len(file_parts) > 1 and file_parts[-1] == file_type:
                j2_files.append(ele)

    return j2_files


def compare_outputs():
    """
    This will compare the configs by rendering the template. 1. sort 2. trim 3. compares the complete config.
    :return:
    """
    old_config = generate_config("old")
    new_config = generate_config("new")

    old_config_set = sort_and_unique_config(old_config)
    new_config_set = sort_and_unique_config(new_config)

    return old_config_set == new_config_set


def generate_config(config_type):
    base_dir_name = os.getcwd() + "/" + config_type
    templates = get_j2files_from_dir(base_dir_name, "j2")
    input_data = get_input_data(base_dir_name + "/data.json")
    return render_jinja_template(base_dir_name, templates, input_data, base_dir_name + "/output.txt")


def sort_and_unique_config(config):
    config_set = set()
    config_lines = config.splitlines()
    for config_line in config_lines:
        trim_line = config_line.strip()
        if trim_line:
            config_set.add(trim_line)

    return sorted(config_set)


if __name__ == "__main__":
    print compare_outputs()
