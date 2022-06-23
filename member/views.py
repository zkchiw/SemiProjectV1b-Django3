from django.shortcuts import render
from member.models import Member
from django.contrib.auth.hashers import make_password
# Create your views here.

# 회원가입 처리 함수 join

def join(request):
    returnPage = 'member/join.html'

    if request.method =='GET':
        return render (request, returnPage)

    if request.method =='POST':
        # 폼으로 전송된 데이터들을 dict형태로 저장

        form = request.POST.dict()
        # print(form, form['userid']) # 전송된 데이터 확인(콘솔)

        # 유효성 검사 1
        error = '' # 검사 결과 저장용 변수 선언
        if  not (form['userid']and form['passwd']and form['passwdret']and form['name']and form['email']):
            error = '입력값이 누락되었습니다'
        elif (form['passwd']!=form['passwdret']):
            error = '비밀번호가 일치하지 않습니다'
        else :
            # 입력한 회원정보를 Member 객체에 담음
            member = Member(
                userid = form['userid'],
                passwd = make_password(form['passwd']), #make_password로 비밀번호 암호화
                name = form['name'],
                eamil = form['email']
            )
            # Member 객체에 담음 회원정보를 member테이블에 저장
            member.save()

            # 회원가입 성공시 joinok.html 페이지를 출력
            returnPage = 'member/joinok.html'


        # 유효성 검사를 실패하는 경우 오류내용을 join.html에 표시하기 위해 dict 변수에 저장
        # 이미 입력했던 회원정보가 사라지지 않게 하기 위해 form이라는 dict 변수 생성
        context = {'form':form, 'error':error}
        return render (request, returnPage, context)


def login(request):
    return render (request, 'member/login.html')

def myinfo(request):
    return render (request, 'member/myinfo.html')
