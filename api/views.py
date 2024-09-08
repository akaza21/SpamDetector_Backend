from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import User, Contact, SpamReport
from .serializers import UserSerializer, ContactSerializer, SpamReportSerializer, SearchResultSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SpamReportViewSet(viewsets.ModelViewSet):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)

class SearchViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        query = request.query_params.get('q', '')
        search_type = request.query_params.get('type', 'name')

        if search_type == 'name':
            results = self.search_by_name(query)
        elif search_type == 'phone':
            results = self.search_by_phone(query)
        else:
            return Response({"error": "Invalid search type"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SearchResultSerializer(results, many=True, context={'request': request})
        return Response(serializer.data)

    def search_by_name(self, query):
        users = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
        contacts = Contact.objects.filter(name__icontains=query)

        results = []
        for user in users:
            results.append({
                'name': user.get_full_name() or user.username,
                'phone_number': str(user.phone_number),
                'email': user.email,
                'spam_likelihood': self.get_spam_likelihood(user.phone_number)
            })

        for contact in contacts:
            if not any(r['phone_number'] == str(contact.phone_number) for r in results):
                results.append({
                    'name': contact.name,
                    'phone_number': str(contact.phone_number),
                    'email': contact.email,
                    'spam_likelihood': self.get_spam_likelihood(contact.phone_number)
                })

        return sorted(results, key=lambda x: (not x['name'].startswith(query), x['name']))

    def search_by_phone(self, query):
        users = User.objects.filter(phone_number__contains=query)
        contacts = Contact.objects.filter(phone_number__contains=query)

        results = []
        for user in users:
            results.append({
                'name': user.get_full_name() or user.username,
                'phone_number': str(user.phone_number),
                'email': user.email,
                'spam_likelihood': self.get_spam_likelihood(user.phone_number)
            })

        if not results:
            for contact in contacts:
                results.append({
                    'name': contact.name,
                    'phone_number': str(contact.phone_number),
                    'email': contact.email,
                    'spam_likelihood': self.get_spam_likelihood(contact.phone_number)
                })

        return results

    def get_spam_likelihood(self, phone_number):
        total_users = User.objects.count()
        spam_reports = SpamReport.objects.filter(phone_number=phone_number).count()
        return spam_reports / total_users if total_users > 0 else 0