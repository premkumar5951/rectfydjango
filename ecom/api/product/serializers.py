from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer,HyperlinkedRelatedField
from .models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(max_length=None,allow_empty_file=False,allow_null=True,required=False)
    # category= HyperlinkedRelatedField(view_name="catg-detail",read_only=True,many=False)
    class Meta:
        model=Product
        fields=("url","id","name","description","image","category","price","stock")