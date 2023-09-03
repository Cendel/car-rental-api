from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields=['id', 'name', 'subject', 'body', 'email']

        # dökümantasyon bizden kendi belirledigi bir mesaji döndürmemizi istiyor yanit olarak. yani, döndürecegimiz mesaji özellestirecegiz. asagida to-representation fonksiyonunu bu amac icin özellestirecegiz. Normalde buna gerek yok, cünkü default olarak zaten bir yanit gidiyor, fakat dökümantasyona uymak icin bunu yapiyoruz.
        def to_representation(self, instance):  # to_representation fonksiyonu, Django REST framework'ün serializers modülünde kullanılan bir özel metottur ve bu metot, bir model örneğini JSON veya belirtilen veri formatlarına dönüştürmek için kullanılır. Ayrıca, bu fonksiyon, özel dönüşüm işlemleri veya farklı yanıtlar oluşturmak için kullanılabilir. Biz burada yanit olusturmak icin kullandik.
            data = super().to_representation(instance)  # data adında bir değişken oluşturulur ve bu değişken, model örneğini JSON formatına dönüştürmek için super().to_representation(instance) ile çağrılan üst sınıfın (ModelSerializer'ın) to_representation fonksiyonunun sonucunu alır.
            # print(self.context['request'].path)
            if self.context['request'].path == "/contactmessage/visitors/":  # self.context['request'].path ifadesi, geçerli isteğin yolu (path) alınır. Bu, isteğin geldiği URL'i temsil eder.
                return {"message": "Successfully created message", "success": True}  # Eğer isteğin yolu "/contactmessage/visitors/" ile eşleşiyorsa, özel bir yanıt döndürülür. Bu yanıt, "Successfully created message" ve "success: True" içeren bir JSON nesnesidir.
            return data