from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request') if self.context else None
