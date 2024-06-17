from analytics.utils import generate_fine_data
from django.views.generic import TemplateView
from users.models import User


class UserAnalyticsView(TemplateView):
    template_name = "analytics/user_analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(pk=self.kwargs["pk"])
        context["completed_data"] = generate_fine_data(self.kwargs["pk"], is_completed=True)
        context["failed_data"] = generate_fine_data(self.kwargs["pk"], is_completed=False)
        return context
