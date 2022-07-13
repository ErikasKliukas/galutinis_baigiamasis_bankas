from django import forms
from . import models


class DepositForm(forms.ModelForm):
    class Meta:
        model = models.Deposit
        fields = ["amount"]


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = models.Withdrawal
        fields = ["amount"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.status = kwargs.pop('status', None)
        super(WithdrawalForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if self.status.balance < amount:
            raise forms.ValidationError(
                'You can not withdraw more than you balance.'
            )

        return amount

class Transfer(forms.ModelForm):
    class Meta:
        model = models.Transfer
        fields = ["amount", "to_account"]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)
        super(WithdrawalForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if self.account.balance < amount:
            raise forms.ValidationError(
                'You can not transfer more than you balance.'
            )