# random util functions I've written
# mostly taken from https://github.com/DanielOaks/goshu but I don't care about the license
import getpass


def true_or_false(in_str):
    """Returns True/False if string represents it, else None."""
    in_str = in_str.lower()

    if in_str.startswith(('true', 'y', '1', 'on')):
        return True
    elif in_str.startswith(('false', 'n', '0', 'off')):
        return False
    else:
        return None


def is_ok(prompt, blank=''):
    """Prompt the user for yes/no and returns True/False
    Arguments:
    prompt -- Prompt for the user
    blank -- If True, a blank response will return True, ditto for False, the default ''
             will not accept blank responses and ask until the user gives an appropriate
             response
    Returns:
    True if user accepts, False if user does not"""
    while True:
        ok = input(prompt).lower().strip()

        if len(ok) > 0:
            if ok[0] == 'y' or ok[0] == 't' or ok[0] == '1':  # yes, true, 1
                return True
            elif ok[0] == 'n' or ok[0] == 'f' or ok[0] == '0':  # no, false, 0
                return False

        else:
            if blank is True:
                return True
            elif blank is False:
                return False


class GuiManager:
    """Handles generic gui stuff."""

    # input functions
    def get_string(self, prompt, repeating_prompt=None, default=None,
                   confirm_prompt=None, blank_allowed=False,
                   password=False, validate=None):
        """Get a string."""
        if repeating_prompt is None:
            repeating_prompt = prompt

        # echo typed chars vs not doing that
        if password:
            fn = getpass.getpass
        else:
            fn = input

        # confirm value if necessary
        if confirm_prompt is not None:
            val1 = fn(prompt)
            val2 = fn(confirm_prompt)

            while (val1 != val2 or
                   (val1.strip() == '' and not blank_allowed and default is None)
                   or (validate and not validate(val1))):
                val1 = fn(repeating_prompt)
                val2 = fn(confirm_prompt)

            if val1.strip() == '' and default is not None:
                output_value = default
            else:
                output_value = val1

        # else just get a value that is / is not blank
        else:
            output_value = fn(prompt)

            if not blank_allowed or validate:
                if default is not None:
                    output_value = default
                else:
                    while (output_value.strip() == '' or
                           (validate and not validate(output_value))):
                        output_value = fn(repeating_prompt)

        return output_value

    def get_number(self, prompt, repeating_prompt=None, default=None, force_int=False, password=False):
        """Get a number, force_int to force an integer."""
        # parse function, since we repeat it
        def parse_value(val):
            try:
                if force_int or '.' not in val:
                    return int(val)
                else:
                    return float(val)
            except (ValueError, TypeError):
                if (default is not None) and (val.strip() == ''):
                    # we take blank as 'use the default'
                    # just use user-provided default
                    return default
                else:
                    return ''  # user screwed up, we'll ask for another value

        # get initial value
        value = self.get_string(prompt, repeating_prompt, blank_allowed=True, password=password)
        value = parse_value(value.strip())

        # repeat if required
        while not isinstance(value, (int, float)):
            value = self.get_string(repeating_prompt, repeating_prompt)
            value = parse_value(value)

        return value

    def get_bool(self, prompt, repeating_prompt=None, default=None, allow_none=False, password=False):
        """Get a bool, allow_none to allow None."""
        # parse function, since we repeat it
        def parse_value(val):
            if val == '':
                if default is not None or allow_none:
                    return default
            else:
                val = true_or_false(val)

                if val is None:
                    return ''
                else:
                    return val

        # get initial value
        value = self.get_string(prompt, repeating_prompt, blank_allowed=True, password=password)
        value = parse_value(value.strip())

        # repeat if needed
        while value not in (True, False, None):
            value = self.get_string(repeating_prompt, repeating_prompt, blank_allowed=True,
                                    password=password)
            value = parse_value(value.strip())

        return value
