import os
import subprocess
from datetime import datetime
import shutil

_n_traces_path = "tracesPath"
_n_e2_ltePlmnId = 'ltePlmnId'
_n_e2_starting_port = 'e2StartingPort'
_n_e2_is_xapp_enabled = 'isXappEnabled'

_v_parameters_file = "parameters.txt"

_REWRITE_TEXT_FILES = True

if __name__ == '__main__':
    _v_output_dir_name = "/storage/franci/millicar3/"
    working_path = "/home/fgjeci/workspace/ns3-mmwave-millicar/"

    _l_threshold = [-10, -5, 0, 5, 10]
    _l_optimization_type = ['distance', 'sinr']
    _all_loads = [24, 48, 64]
    _all_simulations = []

    _l_command_list = []
    _l_log_files = []

    _v_simulation_index = -1

    for _load in _all_loads:
        _all_simulations.append((0, 'no_relay', _load))
        for _threshold in _l_threshold:
            for _optimization_type in _l_optimization_type:
                _all_simulations.append((_threshold, _optimization_type, _load))

    for _single_sim in _all_simulations:
        _threshold = _single_sim[0]
        _optimization_type = _single_sim[1]
        _load = _single_sim[2]
        # change the execution file in base of the load
        _exec_file_name = "vehicular-5g-{}".format(_load)

        _v_sim_tag_name = "threshold_" + str(_threshold) + \
                          "_optimization_type_" + str(_optimization_type) + \
                          "_load_" + str(_load)

        _v_simulation_index += 1


        _v_param_map = {
            _n_traces_path: os.path.join(_v_output_dir_name, _v_sim_tag_name),
            _n_e2_is_xapp_enabled: not (_optimization_type == 'no_relay'),
            _n_e2_ltePlmnId: str(111 + _v_simulation_index),
            _n_e2_starting_port: 48470 + 100 * _v_simulation_index
        }

        _v_param_single_str = " ".join(
            "--{!s}={!s}".format(key, val) for (key, val) in _v_param_map.items())

        _v_sim_directory = _v_output_dir_name

        # Deleting the directory to remove old content
        if _REWRITE_TEXT_FILES:
            if os.path.isdir(os.path.join(_v_sim_directory, _v_sim_tag_name)):
                shutil.rmtree(os.path.join(_v_sim_directory, _v_sim_tag_name))

        _v_sim_directory = os.path.join(_v_output_dir_name, _v_sim_tag_name)

        # check if it exists and create it if it does not exist
        if _REWRITE_TEXT_FILES:
            if not os.path.isdir(_v_sim_directory):
                os.mkdir(_v_sim_directory)

        # Writing data in the parameters file
        _t_parameters_file = open(os.path.join(_v_sim_directory, _v_parameters_file), "w")
        _t_parameters_file.write("std::string {} = {};\n".format(_n_traces_path, _v_sim_directory))
        _t_parameters_file.write(
            "bool {} = {};\n".format(_n_e2_is_xapp_enabled, not (_optimization_type == 'no relay')))
        _t_parameters_file.write("std::string {} = {};\n".format(_n_e2_ltePlmnId, str(111 + _v_simulation_index)))
        _t_parameters_file.write("uint16_t {} = {};\n".format(_n_e2_starting_port, 38470 + 100 * _v_simulation_index))
        _t_parameters_file.close()

        _t_readme_text_file = open(os.path.join(_v_sim_directory, "README.txt"), "w")
        _t_readme_text_file.write("Traces path n: {}\n".format(_v_sim_directory))
        _t_readme_text_file.write("Xapp enabled: {}\n".format(not (_optimization_type == 'no relay')))
        _t_readme_text_file.write("Lte plmn: {}\n".format(str(111 + _v_simulation_index)))
        _t_readme_text_file.write("Port number: {}\n".format(38470 + 100 * _v_simulation_index))
        _t_readme_text_file.write("Load: {}\n".format(_load))
        _v_sim_start_time = datetime.now()
        _t_readme_text_file.write("Simulation starting time: " + str(_v_sim_start_time) + "\n")
        _t_readme_text_file.write("Command: \n")
        _t_readme_text_file.write('./ns3' + ' run ' + r"{} {!s}".format(_exec_file_name, _v_param_single_str))
        _t_readme_text_file.close()

        _l_command_list.append(['./ns3', 'run', r"{} {!s}".format(_exec_file_name, _v_param_single_str)])
        _l_log_files.append(_v_sim_directory)

    ### Run simulation
    os.chdir(working_path)
    processes = []
    log_files_objs = [open(os.path.join(_log_file_full_path, "logfile.log"), 'w') for _log_file_full_path in
                      _l_log_files]

    _processes_id = []

    for _single_command_ind in range(0, len(_l_command_list)):
        _single_command = _l_command_list[_single_command_ind]
        _output_file = log_files_objs[_single_command_ind]
        p = subprocess.Popen(_single_command,
                             stdout=_output_file,
                             stderr=subprocess.STDOUT,  # This will be routed to stdout
                             )
        _processes_id.append(p.pid)
        processes.append(p)

    for p_ind in range(0, len(processes)):
        p = processes[p_ind]
        p.wait()
        _v_sim_stop_time = datetime.now()
        # Add to read me file
        _t_readme_text_file = open(os.path.join(_l_log_files[p_ind], "README.txt"), "a")
        _t_readme_text_file.write("\n\nSimulation ending time: " + str(_v_sim_stop_time))
        _t_readme_text_file.close()
