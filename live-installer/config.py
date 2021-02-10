import yaml
import os
import subprocess
from glob import glob

def load_config(config_path):
    if os.path.isfile(config_path):
        file = open(config_path, "r")
    else:
        exit("{} doesn't exists. Please create config file!".format(config_path))

    try:
        contents = yaml.load(file, Loader=yaml.FullLoader)
    except:
        contents = yaml.load(file)
    return contents


main = load_config("configs/config.yaml")

if(main["distribution"] == "auto"):
    if(os.path.exists("/etc/debian/release")):
        distro = load_config("configs/distribution/debian.yaml")
else:
    distro = load_config("configs/distribution/{}.yaml".format(main["distribution"]))


# Package Manager
for package_manager in glob("configs/package_managers/*"):
        pm_contents = load_config(package_manager)   

        if os.path.exists(pm_contents["check_this_dir"]):
            pm = pm_contents
            break

def package_manager(process, packages=[]):
    if process == "name":
        exit("You can't use this parameter!")
    if process in pm:
        pkgs = " ".join(str(p) for p in packages)
        cmd = (pm[process] + " ").replace("{packages}", pkgs)

        return cmd
    else:
        exit("Process doesn't exists on package manager's config file!")


# Update Initramfs
def update_initramfs():
    initramfs = load_config("configs/initramfs_systems/" + main["initramfs_system"] + ".yaml")

    commands = []
    for command in initramfs["commands"]:
        if "{kernel_version}" in command:
            kernel_version= subprocess.getoutput("uname -r")
            command = command.replace('{kernel_version}', kernel_version)

            commands.append(command)
        else:
            commands.append(command)

    return commands


print(package_manager("remove_package_with_unusing_deps", main["remove_packages"]))