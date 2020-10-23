import win32com.client


class ShadowCopy(object):
    def __init__(self, drive_letters):
        """
        Creates shadow copies for each local drive in the set drive_letters.
        """
        self.__drive_letters = set()
        self.__shadow_ids = {}
        self.__shadow_paths = {}

        self.wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")

        for dl in drive_letters:
            self.__add_drive(dl)

    def shadow_path(self, path):
        '''
        Takes a regular file system path and transforms it into an
        equivalent path in a shadow copy
        '''
        drive_letter = path[0]
        if drive_letter in self.__drive_letters:
            new_path = path.replace(drive_letter + ':',
                                    self.__shadow_paths[drive_letter],
                                    1)
            if new_path == path:
                raise Exception("Problem processing path: {0}".format(path))
            return new_path
        else:
            raise Exception("Shadow copy not found for requested drive")

    def unshadow_path(self, path):
        '''
        Takes a shadow copy path and transforms it into an equivalent
        regular file system path with a drive letter
        '''
        for dl, sp in self.__shadow_paths.items():
            if sp in path:
                new_path = path.replace(
                    sp,
                    dl + ":",
                    1)
                if new_path == path:
                    raise Exception(
                        "Problem processing path: {0}".format(path))
                else:
                    return new_path
        raise Exception("Drive letter not found for shadow path")

    def delete(self):
        """
        This method should be called when done using the shadow copies in
        order to release them.
        """
        for shadow_id in self.__shadow_ids.values():
            self.__vss_delete(shadow_id)

    def __add_drive(self, drive_letter):
        if drive_letter not in self.__drive_letters:
            self.__drive_letters.add(drive_letter)
            shadow_id = self.__vss_create(drive_letter)
            shadow_path = self.__vss_list(shadow_id)
            self.__shadow_ids[drive_letter] = shadow_id
            self.__shadow_paths[drive_letter] = shadow_path

    def __vss_get_id(self, shadow_id):
        obj = self.wmi.ExecQuery("SELECT * FROM Win32_ShadowCopy WHERE ID=\"{0}\"".format(shadow_id))
        return obj[0]

    def __vss_list(self, shadow_id):
        return self.__vss_get_id(shadow_id).DeviceObject

    def __vss_create(self, drive_letter):
        sc = self.wmi.get("Win32_ShadowCopy")
        createparams = sc.Methods_("Create").InParameters.SpawnInstance_()
        createparams.Properties_[1].value = "{0}:\\".format(drive_letter)
        results = wmi.ExecMethod_("Create", createparams)
        return results.Properties_[1].value

    def __vss_delete(self, shadow_id):
        self.__vss_get_id(shadow_id).Delete_()