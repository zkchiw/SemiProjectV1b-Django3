from django.shortcuts import render, redirect
import board
from board.models import Board
from member.models import Member

# 게시판 목록보기 처리

def list(request):
    bdlist = Board.objects.values('id','title','userid','regdate','views').order_by('-id')
    context = {'bds':bdlist}

    return render (request, 'board/list.html',context)

# 게시판 본문보기 처리
def view(request):
    return render (request, 'board/view.html')

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
                userid= Member.objects.get(pk=form['userid'])
            )
            bd.save()
            return redirect('/list')

        context = {'form': form, 'error': error}
        return render(request, returnPage, context)