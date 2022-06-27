from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control

import board
from board.models import Board
from member.models import Member

# 게시판 목록보기 처리

# 데코레이터로 웹페이지의 캐시기능을 중지
@cache_control(no_chche=True, no_store=True, must_revalidate=True)
def list(request):
    # bdlist = Board.objects.values('id','title','userid','regdate','views').order_by('-id')

    # Board와 Member테이블은 userid <-> id 컬럼을 기준으로 inner join을 수행
    bdlist = Board.objects.select_related('member')

    # join된 member테이블의 userid확인
    # bdlist.get(0).member.userid
    context = {'bds':bdlist}
    return render (request, 'board/list.html',context)

# 게시판 본문보기 처리
def view(request):
    if request.method=='GET':
        form = request.GET.dict()
    # print(form['bno'])

        #본문글에 대한 조회수 증가
        # b= Board.objects.get(id=form['bno'])
        # b.views=b.views+1
        # b.save()
        from django.db.models import F
        Board.objects.filter(id=form['bno']).update(views=F('views')+1)

        # 본문글 조회
        bd = Board.objects.select_related('member')\
            .get(id=form['bno'])
    elif request.method=='POST':
        pass

    context ={ 'bd': bd}
    return render (request, 'board/view.html',context)

# 게시판 글쓰기 처리
# get : board/write.html
# post : 작성한 글을 db에 저장, board/list.html로 이동
def write(request):
    returnPage = 'board/write.html'
    error = ''
    form = ''
    if request.method == 'GET':
        return render(request, returnPage)

    elif request.method == 'POST':
        form = request.POST.dict()

        # 유효성 검사

        if (not form['title'] and form['contents']):
            error = '제목이나 본문을 작성하세요'
        else:
            # 입력한 게시글을 Board객체에 담음
            bd = Board(
                title=form['title'],
                contents=form['contents'],
                # 새글을 작성한 회원에 대한 정보는
                # 회원테이블에 존재하는 회원번호를 조회해서 userid속성에 회원번호저장
                member= Member.objects.get(pk=form['memberid'])
            )
            bd.save()
            return redirect('/list')

        context = {'form': form, 'error': error}
        return render(request, returnPage, context)


# 게시글 삭제
# /remove?bno=????
def remove(request):
    if request.method=='GET':
        form = request.GET.dict()
        Board.objects.filter(id=form['bno']).delete()
    return redirect('/list')

# 게시글 본문 수정
def modify(request):

    if request.method=='GET':
        form = request.GET.dict()
        bd =Board.objects.get(id=form['bno'])

    elif request.method=='POST':
        form = request.POST.dict()
        # b = Board.objects.get(id=form['bno'])
        # b.title = form['title']
        # b.contents = form['contents']
        # b.save()
        Board.objects.filter(id=form['bno']).update(title=form['title'], contents=form['contents'])
        return redirect('/view?bno='+form['bno'])
    context = {'bd': bd}
    return render(request, 'board/modify.html', context)