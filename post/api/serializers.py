from django.db.models import Count, Avg
from rest_framework import serializers

from post.models import Post, UserPostScore


class PostSerializer(serializers.ModelSerializer):
    score_count = serializers.SerializerMethodField('get_scores_count')
    score_average = serializers.SerializerMethodField('get_scores_average')
    user_score = serializers.SerializerMethodField('get_user_score')

    def get_scores_count(self, obj):
        return obj.scores.aggregate(count=Count('score')).get('count', 0)

    def get_scores_average(self, obj):
        average = obj.scores.aggregate(average=Avg('score')).get('average', 0)
        return round(average, 1) if average else average

    def get_user_score(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return None
        score = obj.scores.filter(user=user).first()
        if score:
            return score.score
        return None

    class Meta:
        model = Post
        fields = ('id', 'title', 'score_count', 'score_average', 'user_score')


class PostScoreSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        post_score, created = UserPostScore.objects.update_or_create(
            user=validated_data.get('user'), post=validated_data.get('post'),
            defaults={'score': validated_data.get('score')}
        )
        return post_score

    class Meta:
        model = UserPostScore
        fields = ('score',)
