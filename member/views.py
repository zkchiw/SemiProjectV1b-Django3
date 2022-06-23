from member.models import Member
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect

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

        # 유효성 검사
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
                email = form['email']
            )
            # Member 객체에 담음 회원정보를 member테이블에 저장
            member.save()

            # 회원가입 성공시 joinok.html 페이지를 출력
            returnPage = 'member/joinok.html'


        # 유효성 검사를 실패하는 경우 오류내용을 join.html에 표시하기 위해 dict 변수에 저장
        # 이미 입력했던 회원정보가 사라지지 않게 하기 위해 form이라는 dict 변수 생성
        context = {'form':form, 'error':error}
        return render (request, returnPage, context)

# 로그인 처리 함수 login
def login(request):
    returnPage = 'member/login.html'
    if request.method == 'GET':
        return render(request, returnPage)

    elif request.method == 'POST':
        form = request.POST.dict()
        error = ''
        if  not (form['userid']and form['passwd']):
            error = '아이디와 비밀번호를 입력해 주세요'
        else:
            # 입력한 아이디로 회원정보가 테이블에 존재하는지 여부 확인

            try:
                member = Member.objects.get(userid=form['userid'])
            except Member.DoesNotExist:
                member=None

            if member and check_password(form['passwd'],member.passwd):
                # 아이디와 비밀번호 인증을 정상적으로 마쳤다면 세션 변수에 인증정보를 저장해둠
                request.session['userid'] = form['userid']

                return redirect('/') # index 페이지로 이동
            else :
                error= '아이디나 비밀번호가 일치하지 않습니다'

        context = {'error':error}
        return render(request, returnPage, context)


# 로그인한 회원 정보 출력 함수 myinfo
def myinfo(request):
    # 로그인한 회원 아이디를 알아냄 - 세션변수
    member = {}

    if request.session.get('userid'):
        userid = request.session.get('userid')

    # 아이디를 이용해서 member 테이블에서 회원정보를 조회
        member =Member.objects.get(userid=userid)

    context = {'member':member}
    return render (request, 'member/myinfo.html',context)

# 로그아웃 처리 함수
def logout(request):
    # 만약 세션변수 userid가 존재하면 세션변수 삭제
    if request.session.get('userid') :
        del(request.session['userid'])

    # 로그아웃시 index로 이동
    return redirect('/')