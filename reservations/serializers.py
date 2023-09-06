from rest_framework import serializers
from cars.serializers import CarSerializer
from cars.models import Car
from decimal import Decimal  # decimal.Decimal, Python programlamada kullanılan bir veri türüdür ve ondalık sayıları tam ve kesirli olarak işlemek için kullanılır. Bu modül, kayan nokta (float) sayılarının bazı hassasiyet sorunlarını aşmak ve finansal hesaplamalarda daha doğru sonuçlar elde etmek için kullanılır.
from datetime import datetime
from dateutil import parser  # (bunun icin pip install yapmak gerekli) -  dateutil.parser, Python'da tarih ve saat bilgilerini ayrıştırmak ve oluşturmak için kullanılan bir modül ve alt modüldür. Bu modül, tarih ve saat bilgilerini metin (string) formatından Python'da işlenebilir veri türlerine dönüştürmek için kullanılır. Ayrıca, belirli bir tarih ve saat formatına sahip metinleri tarih ve saat nesnelerine dönüştürmeye olanak tanır.
from datetime import timezone  # datetime modülü, Python'da tarih ve saatle ilgili işlemleri yapmak için kullanılır.
from .models import Reservation
from django.utils import timezone
import math


class ReservationSerializer(serializers.ModelSerializer):
    # Nested CarSerializer on read
    car = CarSerializer(read_only=True)

    car_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    # CarField on write
    # car_id = serializers.PrimaryKeyRelatedField(
    #     write_only=True,
    #     source='car',
    #     queryset=Car.objects.all(),
    #     label='Car')
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ('id', 'car', 'pickUpTime', 'dropOffTime', 'car_id', 'user_id'
                  , 'pickUpLocation', 'dropOffLocation', 'status', 'totalPrice', 'userId')
        extra_kwargs = {
            'totalPrice': {'read_only': True},
            'status': {'read_only': True}
        }

    def get_userId(self, obj):
        return obj.user.id

    def validate_pickUpTime(self, value):

        if value <= timezone.now():
            raise serializers.ValidationError("pickUpTime must be greater than the current time.")
        return value

    def validate_dropOffTime(self, value):

        pick_up_time = self.initial_data.get('pickUpTime')

        if value <= parser.parse(pick_up_time).replace(tzinfo=timezone.utc):
            raise serializers.ValidationError("dropOffTime must be greater than pickUpTime.")
        return value

    def validate(self, attrs):
        pick_up_time = attrs['pickUpTime']
        drop_off_time = attrs['dropOffTime']
        car_id = attrs['car_id']

        # asagida bir ORM filtrelemesi yapiyoruz (asagidaki pickUpTime__lt ve dropOffTime__gt ifadeleri, Django ORM'deki filtreleme sorgularını temsil ediyor)
        overlapping_reservations = Reservation.objects.filter(  # overlapping_reservations, mevcut rezervasyonlar arasında çakışan rezervasyonları bulmak için kullanılan bir sorgu oluşturur. Bu sorgu, aynı araçla ilgili olan ve belirtilen pick_up_time ile drop_off_time aralığında olan rezervasyonları seçer.
            car_id=Car.objects.get(id=car_id),  # önce arac id'sine göre filtreliyoruz cünkü bu araca ait rezervasyonlar icerisinde asagidaki filtreleme islemine devam edecegiz
            pickUpTime__lt=drop_off_time,  # Bu ifade, "pickUpTime" adlı bir alanın "drop_off_time" değişkeninden küçük (less than) olduğu durumları seçer. Yani "pickUpTime" değeri, "drop_off_time" değerinden önce olan rezervasyonları seçer.
            dropOffTime__gt=pick_up_time  # Bu ifade, "dropOffTime" adlı bir alanın "pick_up_time" değişkeninden büyük (greater than) olduğu durumları seçer. Yani "dropOffTime" değeri, "pick_up_time" değerinden sonra olan rezervasyonları seçer.
        )

        if self.instance:  # self.instance, Django REST framework (DRF) serileştiricilerinde (serializers) sıklıkla kullanılan bir özelliktir. Bu özellik, serileştirici içerisinde işlem yapılan nesneyi temsil eder. Yani, self.instance ifadesi, serileştirici tarafından işlenen veritabanı nesnesini temsil eder. Özellikle güncelleme işlemlerinde kullanılır. Eğer bir nesne güncelleniyorsa, self.instance bu nesneyi temsil eder
            # yukaridaki satirda, eger güncellestirme yapiliyorsa dedik.. eger güncellestirme yapiliyorsa, asagidaki satirdaki kodla, bu güncellestirme isleme sirasinda bu güncellestirilen nesneyi validate islemine sokma diyecegiz
            overlapping_reservations = overlapping_reservations.exclude(pk=self.instance.pk)

        if overlapping_reservations.exists():
            raise serializers.ValidationError("Reservation overlaps with existing reservations.")

        return attrs

    def create(self, validated_data):
        try:
            car_id = validated_data['car_id']
            car = Car.objects.get(id=car_id)
            pick_up_time = validated_data['pickUpTime']
            drop_off_time = validated_data['dropOffTime']
            price_per_hour = float(car.pricePerHour)

            # Calculate total hours
            total_hours = (drop_off_time - pick_up_time).total_seconds() / 3600

            # Calculate total price
            total_price = Decimal(total_hours) * Decimal(price_per_hour)

            validated_data['totalPrice'] = total_price

            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError(f'{e}')

    def update(self, instance, validated_data):
        car_id = validated_data['car_id']
        car = Car.objects.get(id=car_id)
        pick_up_time = validated_data['pickUpTime']
        drop_off_time = validated_data['dropOffTime']
        price_per_hour = float(car.pricePerHour)

        # Calculate total hours
        total_hours = (drop_off_time - pick_up_time).total_seconds() / 3600

        # Calculate total price
        total_price = Decimal(total_hours) * Decimal(price_per_hour)

        validated_data['totalPrice'] = total_price
        return super().update(instance, validated_data)



