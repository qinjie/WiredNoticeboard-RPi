import ConfigParser
import datetime
import json
import os


def read_config(filepath):
    if not os.path.exists(filepath):
        print 'Missing device configuration file.'
        return {}
    else:
        with open(filepath, 'rb') as f:
            str = f.read()
            return json.loads(str)


def turn_on_hdmi():
    os.system("tvservice -p")
    os.system("sudo chvt 9")
    os.system("sudo chvt 7")


def turn_off_hdmi():
    os.system("tvservice -o")


def read_ini(ini_file):
    parser = ConfigParser.SafeConfigParser()
    parser.read(ini_file)
    parser.defaults()
    base_url = parser.get('default', 'url_base')
    urls = {}
    urls['device_enroll'] = base_url + parser.get('default', 'device_enroll')
    urls['device_playlist'] = base_url + parser.get('default', 'device_playlist')
    urls['device_download'] = base_url + parser.get('default', 'device_download_file')
    return urls


if __name__ == '__main__':

    CONFIG_FILE = 'device.json'
    _path_cur_dir = os.path.dirname(os.path.realpath(__file__))
    _file_config = os.path.join(_path_cur_dir, CONFIG_FILE)

    config_json = read_config(_file_config)
    if (not config_json['turn_on_time']) and (not config_json['turn_on_time']):
        print "No turn_on_time and turn_off_time setting found."
        exit(1)

    turn_on_time = datetime.datetime.strptime(config_json['turn_on_time'], "%H:%M:%S").time()
    turn_on_date_time = datetime.datetime.combine(datetime.datetime.today(), turn_on_time)

    turn_off_time = datetime.datetime.strptime(config_json['turn_off_time'], "%H:%M:%S").time()
    turn_off_date_time = datetime.datetime.combine(datetime.datetime.today(), turn_off_time)

    cur_time = datetime.datetime.time(datetime.datetime.now())

    print "Current Time: {}".format(cur_time)
    print "ON Time: {}".format(turn_on_time)
    print "OFF Time: {}".format(turn_off_time)

    if turn_on_time < turn_off_time:
        if cur_time < turn_on_time or cur_time > turn_off_time:
            turn_off_hdmi()
        elif cur_time > turn_on_time and cur_time < turn_off_time:
            turn_on_hdmi()
    elif turn_on_time > turn_off_time:
        if cur_time < turn_off_time or cur_time > turn_on_time:
            turn_on_hdmi()
        elif cur_time > turn_off_time and cur_time < turn_on_time:
            turn_off_hdmi()
