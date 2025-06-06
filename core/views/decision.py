import json

from core.models.Decision import Decision
from core.shared.HybridRenderView import HybridRenderView
from core.forms.decision import DecisionForm
from rest_framework import serializers

import accounts.models.User as User
from django.shortcuts import get_object_or_404, redirect, render

class UserShortNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid','preferred_name')

class DecisionSidebarSerializer(serializers.ModelSerializer):
    responsible = UserShortNameSerializer()
    class Meta:
        model = Decision
        fields = ['uid', 'summary', 'responsible']


class DecisionSelectionList(HybridRenderView):
    template_name = 'decisions/main.html'  # adjust as needed

    def get(self, request):
        decisions = Decision.objects.select_related('responsible').all().only('uid', 'summary', 'responsible__preferred_name', 'created_at', 'adopted_date')
        data = DecisionSidebarSerializer(decisions, many=True).data
        context = {'decisions': data, "table_data": json.dumps(data) }

        return self.render_response(request, context)

class DecisionEdit(HybridRenderView):

    def get(self, request, uid):
        decision = get_object_or_404(Decision, uid=uid)
        form = DecisionForm(instance=decision)
        return render(request, 'decisions/edit.html', {'form': form, 'decision': decision})



# class DecisionSidebarListView(generics.ListAPIView):
#     queryset = Decision.objects.all().only('id', 'resolution')
#     serializer_class = DecisionSidebarSerializer