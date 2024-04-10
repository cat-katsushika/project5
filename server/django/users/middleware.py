from django.shortcuts import redirect


class CustomAdminAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 管理画面へのアクセスかつカスタム認証がまだなら認証ページへリダイレクト
        if request.path.startswith(
            "/admin/KOgEdTnMXbsDJa8jK347oaVqVzbshgIfhOWBjim9uEA5RfsEpl/"
        ) and not request.session.get("custom_admin_auth", False):
            return redirect("/custom-admin-auth/")
        response = self.get_response(request)
        return response
