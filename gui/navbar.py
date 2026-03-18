import customtkinter as ctk
import theme

class Navbar(ctk.CTkFrame):
    def __init__(self, parent, controller, buttons):
        """
        buttons: list of tuples (display_text, view_name)
        """
        super().__init__(parent, fg_color=theme.PRIMARY, width=200, corner_radius=0)
        self.controller = controller
        self.buttons = buttons
        self.button_widgets = {}

        self.grid_propagate(False)

        # Logo
        logo = ctk.CTkLabel(self, text="PAMS", font=("Helvetica", 28, "bold"), text_color="white")
        logo.pack(pady=(30, 40))

        # Create nav buttons
        for text, view_name in buttons:
            btn = ctk.CTkButton(
                self,
                text=text,
                command=lambda v=view_name: self.controller.show_view(v),
                fg_color="transparent",
                hover_color=theme.PRIMARY_DARK,
                text_color="white",
                anchor="w",
                height=40,
                corner_radius=0
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.button_widgets[view_name] = btn

        # Logout button at bottom
        logout_btn = ctk.CTkButton(
            self,
            text="Logout",
            command=self.controller.logout,
            fg_color="transparent",
            hover_color="#7a070d",
            text_color="white",
            anchor="w",
            height=40,
            corner_radius=0
        )
        logout_btn.pack(fill="x", padx=10, pady=(20, 10), side="bottom")

    def highlight(self, view_name):
        """Highlight the active button"""
        for name, btn in self.button_widgets.items():
            if name == view_name:
                btn.configure(fg_color=theme.PRIMARY_DARK)
            else:
                btn.configure(fg_color="transparent")