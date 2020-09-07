import logging
import os
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter.ttk import *
import sys

from classes.intersection import IntersectionWithError
from classes.point import Point
from classes.throw import Throw

logger = logging.getLogger('GUI')

# See https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#run-time-information
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


class EyeLinerApp(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.style = Style()
        logger.info(f"Themes available: {self.style.theme_names()}")
        self.style.theme_use("vista")

        self.wm_title('EyeLiner')
        self.iconbitmap(default=os.path.join(bundle_dir, "icon.ico"))
        self.setup_ui()

        self.geometry(f'350x300')
        self.minsize(350, 300)
        # self.resizable(False, False)

        self.throws = []

    def setup_ui(self):
        self.columnconfigure(0, weight=1, minsize=150)
        self.columnconfigure(1, weight=3, minsize=180)
        self.rowconfigure(0, weight=1, minsize=300)

        self.label_frame = LabelFrame(self, text='Throws', padding=5)
        # self.label_frame.pack(fill=BOTH, expand='yes')
        self.label_frame.grid(
            row=0, column=0,
            padx=10, pady=10,
            sticky=E + W + N + S,
        )

        self.throws_listbox = Listbox(self.label_frame, activestyle=NONE)
        self.throws_listbox.pack(fill=BOTH, expand=YES)
        self.throws_listbox.bind('<Double-Button>', self.edit_throw)

        self.buttons_frame = Frame(self.label_frame)
        self.buttons_frame.pack(fill=X, pady=5, side=TOP)
        # self.buttons_frame.grid(row=1, column=0)

        self.add_throw_button = Button(
            self.buttons_frame, text='+',
            width=8,
            command=self.show_popup,
        )
        self.remove_throw_button = Button(
            self.buttons_frame, text='−',
            width=3,
            command=self.delete_selected_throw,
        )
        self.clear_throws_button = Button(
            self.buttons_frame, text='c',
            width=3,
            command=self.clear_throws,
        )
        self.buttons_frame.columnconfigure(0, weight=4)
        self.buttons_frame.columnconfigure(1, weight=2)
        self.buttons_frame.columnconfigure(2, weight=2)
        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.rowconfigure(1, weight=0)
        self.add_throw_button.grid(
            row=0, column=0,
            sticky=E + W + N + S,
        )
        self.remove_throw_button.grid(
            row=0, column=1,
            # sticky=E + W + N + S,
        )
        self.clear_throws_button.grid(
            row=0, column=2,
            # sticky=E + W + N + S,
        )

        self.calculation_frame = LabelFrame(self, text='Intersection', padding=3)
        self.calculation_frame.grid(
            row=0, column=1,
            rowspan=2,
            padx=10, pady=10,
            sticky=E + W + N + S,
        )

        self.calculate_intersection_button = Button(
            self.calculation_frame,
            text='Calculate',
            command=self.calculate_intersection,
        )
        self.calculate_intersection_button.pack(fill=X)

        Separator(
            self.calculation_frame,
            orient=HORIZONTAL,
        ).pack(pady=5, fill=X)

        # self.calculation_frame.columnconfigure(0, weight=0)
        # self.calculation_frame.columnconfigure(1, weight=2)
        # self.calculation_frame.rowconfigure(0, weight=1)
        # self.calculation_frame.rowconfigure(1, weight=0)

        self.calc_values_frame = Frame(self.calculation_frame)
        self.calc_values_frame.pack(expand=True, fill=BOTH)

        self.range_font = Font(size=8)

        self.calc_x_frame = Frame(self.calc_values_frame)
        self.calc_x_frame.pack(pady=5)

        self.calc_x = Label(self.calc_x_frame, text="X: ")
        self.calc_x.grid(row=0, column=0)
        self.calc_x_value = Label(self.calc_x_frame, text="None")
        self.calc_x_value.grid(row=0, column=1)

        self.calc_x_range = Label(self.calc_x_frame, text='From ... to ...', font=self.range_font)
        self.calc_x_range.grid(row=1, column=0, columnspan=2)

        self.calc_z_frame = Frame(self.calc_values_frame)
        self.calc_z_frame.pack(pady=5)
        self.calc_z = Label(self.calc_z_frame, text="Z: ")
        self.calc_z.grid(row=0, column=0)
        self.calc_z_value = Label(self.calc_z_frame, text="None")
        self.calc_z_value.grid(row=0, column=1)

        self.calc_z_range = Label(self.calc_z_frame, text='From ... to ...', font=self.range_font)
        self.calc_z_range.grid(row=1, column=0, columnspan=2)

    def refresh_throws_listbox(self):
        self.throws_listbox.delete(0, END)
        for throw in self.throws:
            self.throws_listbox.insert(
                END,
                use_minus(
                    f' X: {throw.point.x:.1f},'
                    f' Z: {throw.point.z:.1f},'
                    f' F: {throw.facing:.1f}'
                )
            )

    def show_popup(self):
        ThrowEditor(self, self.add_throw)

    def add_throw(self, throw: Throw):
        logger.info(f"Adding throw: {throw}")
        self.throws.append(throw)
        self.refresh_throws_listbox()

    def edit_throw(self, event=None):
        current_selection = self.throws_listbox.curselection()
        if len(current_selection) == 1:
            selected_i = current_selection[0]
            ThrowEditor(
                self,
                callback=lambda edited_throw: self.set_throw(selected_i, edited_throw),
                initial_throw=self.throws[selected_i],
            )

    def set_throw(self, i: int, throw: Throw):
        logger.info(f"Setting throw {i} to {throw} from {self.throws[i]}")
        self.throws[i] = throw
        self.refresh_throws_listbox()

    def delete_selected_throw(self):
        current_selection = self.throws_listbox.curselection()
        self.throws = [
            throw
            for i, throw in enumerate(self.throws)
            if i not in current_selection
        ]
        self.refresh_throws_listbox()

    def clear_throws(self):
        if messagebox.askokcancel("Clear throws", "Clear all throws?"):
            logging.info(f"Clearing all throws.")
            self.throws = []
            self.refresh_throws_listbox()

    def calculate_intersection(self):
        try:
            intersection = IntersectionWithError.from_throws(self.throws)
            logger.info(f"Calculated intersection: {intersection}")
            self.calc_x_value.config(text=use_minus(f"{intersection.point.x:.1f}"))
            self.calc_z_value.config(text=use_minus(f"{intersection.point.z:.1f}"))

            self.calc_x_range.config(
                text=use_minus(f"From {intersection.x_range[0]:.1f} to {intersection.x_range[1]:.1f}")
            )
            self.calc_z_range.config(
                text=use_minus(f"From {intersection.z_range[0]:.1f} to {intersection.z_range[1]:.1f}")
            )
        except Exception as e:
            messagebox.showerror(f"Error calculating intersection", e)


class ThrowEditor(Toplevel):
    def __init__(self, parent, callback, *args, initial_throw: Throw = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.callback = callback
        self.initial_throw = initial_throw

        self.wm_title("Throw")
        self.transient(parent)

        self.setup_ui()
        if self.initial_throw:
            self.set_throw(self.initial_throw)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        x = self.parent.winfo_x()
        y = self.parent.winfo_y()
        self.geometry(f'180x100+{x + 25}+{y + 25}')
        self.resizable(False, False)

        # Take focus
        self.grab_set()
        self.focus_set()
        self.wait_window(self)

    def setup_ui(self):
        self.columnconfigure(0, weight=0, minsize=50)
        self.columnconfigure(1, weight=1, minsize=50, pad=50)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.validate_command = self.register(self.validate_number)

        self.x_label = Label(self, text='X')
        self.x_label.grid(
            row=0, column=0,
            padx=10,
            pady=5,
        )
        self.x_entry = Entry(
            self,
            validate='key',
            validatecommand=(self.validate_command, '%P'),
        )
        self.x_entry.grid(
            row=0, column=1,
            padx=10,
            pady=5,
            sticky=E + W,
        )

        self.z_label = Label(self, text='Z')
        self.z_label.grid(
            row=1, column=0,
            padx=10,
            pady=5,
        )
        self.z_entry = Entry(
            self,
            validate='key',
            validatecommand=(self.validate_command, '%P'),
        )
        self.z_entry.grid(
            row=1, column=1,
            padx=10,
            pady=5,
            sticky=E + W,
        )

        self.facing_label = Label(self, text='Facing')
        self.facing_label.grid(
            row=2, column=0,
            padx=10,
            pady=5,
        )
        self.facing_entry = Entry(
            self,
            validate='key',
            validatecommand=(self.validate_command, '%P'),
        )
        self.facing_entry.grid(
            row=2, column=1,
            padx=10,
            pady=5,
            sticky=E + W,
        )

    def set_throw(self, throw: Throw):
        self.x_entry.delete(0, END)
        self.x_entry.insert(0, f"{throw.point.x:.3f}")
        self.z_entry.delete(0, END)
        self.z_entry.insert(0, f"{throw.point.z:.3f}")
        self.facing_entry.delete(0, END)
        self.facing_entry.insert(0, f"{throw.facing:.1f}")

    @staticmethod
    def validate_number(new_string):
        if new_string == "" or new_string == "-":
            return True
        try:
            float(new_string)
            return True
        except ValueError:
            logger.warning(f"Rejecting change as cannot convert to float: {new_string}")
            return False

    def ok(self, event=None):
        x_entry = self.x_entry.get()
        z_entry = self.z_entry.get()
        facing_entry = self.facing_entry.get()

        errors = []
        if not x_entry:
            errors.append("x_entry is empty")
        else:
            try:
                x_entry_float = float(x_entry)
            except ValueError:
                errors.append(f"x_entry ({x_entry}) cannot be converted to float")

        if not z_entry:
            errors.append("z_entry is empty")
        else:
            try:
                z_entry_float = float(z_entry)
            except ValueError:
                errors.append(f"z_entry ({z_entry}) cannot be converted to float")

        if not facing_entry:
            errors.append("facing_entry is empty")
        else:
            try:
                facing_entry_float = float(facing_entry)
                if facing_entry_float > 180 or facing_entry_float < -180:
                    errors.append(f"facing_entry ({facing_entry}) should be between -180 and 180.")
            except ValueError:
                errors.append(f"facing_entry ({facing_entry}) cannot be converted to float")

        if errors:
            error_message = f"Rejecting throw entry due to errors: {', '.join(errors)}"
            logger.error(error_message)
            messagebox.showerror("Invalid entry", error_message)
            return

        self.withdraw()
        self.update_idletasks()

        self.callback(
            Throw(
                point=Point(x_entry_float, z_entry_float),
                facing=facing_entry_float,
            )
        )

        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()


def use_minus(string: str):
    return string.replace("-", "−")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    EyeLinerApp().mainloop()
