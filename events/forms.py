from django import forms
from .models import Event, EventRegistration
from .models import ClubMember
from django.contrib.auth.models import User


class EventForm(forms.ModelForm):

    class Meta:

        model = Event

        fields = [
            "name",
            "description",
            "image",
            "date",
            "start_time",
            "end_time",
            "category",
            "venue",
            "participants",
            "registration_fee",
            "registration_type",
            "registration_link",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe your event",
                    "rows": 4,
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "start_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "end_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "venue": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "participants": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Maximum participants",
                    "min": "1",
                }
            ),

            "registration_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0 for free event",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "registration_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "registration_link": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://...",
                }
            ),
        }
    def clean(self):

        cleaned_data = super().clean()

        registration_type = cleaned_data.get("registration_type")
        registration_link = cleaned_data.get("registration_link")

        if registration_type == "EXTERNAL" and not registration_link:
            self.add_error(
                "registration_link",
                "Please provide the external registration link."
            )

        return cleaned_data

class EventRegistrationForm(forms.ModelForm):

    class Meta:
        model = EventRegistration

        fields = [
            "name",
            "usn",
            "branch",
            "semester",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your name",
                }
            ),

            "usn": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your USN",
                }
            ),

            "branch": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your branch",
                }
            ),

            "semester": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your semester",
                    "min": "1",
                    "max": "8",
                }
            ),
        }

class AddCoreMemberForm(forms.Form):

    position = forms.CharField(
        max_length=100,
        label="Position",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Example: Event Lead",
            }
        )
    )

    def clean_position(self):
        position = self.cleaned_data["position"].strip()

        if position.lower() == "president":
            raise forms.ValidationError(
                "President is assigned separately and cannot be added as a core-member position."
            )

        return position

class StudentSearchForm(forms.Form):

    search = forms.CharField(
        max_length=100,
        required=True,
        label="Student Name or USN",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter student name or USN",
            }
        )
    )



from django import forms
from .models import Club


class ClubEditForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ["name", "description", "logo"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),
            "logo": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
        }



