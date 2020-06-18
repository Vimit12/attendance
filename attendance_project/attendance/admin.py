from django.contrib import admin
from .models import *

# class FinancialYearModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'session_start_year', 'session_end_year']
    

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'admin', 'emp_id',
                    'gender', 'address', 'created_at', 'updated_at']
    

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'emp_id_attendance', 'attendance_date',
                    'created_at',  'updated_at']
    

# class AttendanceReportMonthlytAdmin(admin.ModelAdmin):
#     list_display = ['id', 'emp_id_report', 'month',
#                       'created_at', 'updated_at']
    

class LeaveReportEmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'emp_id_leave', 'attendance_id_leave', 'from_leave_date', 'to_leave_date',
                    'leave_message', 'leave_status', 'created_at', 'updated_at']


admin.site.register(Profile)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
# admin.site.register(AttendanceReportMonthly, AttendanceReportMonthlytAdmin)
admin.site.register(LeaveReportEmployee, LeaveReportEmployeeAdmin)

