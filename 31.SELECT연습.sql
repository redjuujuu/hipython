# 주문내역정보를 출력 - 제품번호, 단가, 주문수량, 할인율, 주문금액
use wntrade;
select 제품번호
, 단가 
, 주문수량
, 할인율
, 단가*주문수량 as 주문금액
from 주문세부;

#단일행 함수
1. 문자함수
2. 숫자함수
3. 날짜함수
--집계함수

USE WNTRADE;
SELECT FIELD('JAVA', 'SQL', 'JAVA', 'C')
, FIND_IN_SET('JAVA', 'SQL,JAVA,C')
, INSTR('네 인생을 찾아라', '인생')
,LOCATE('인생', '네 인생을 살아라');


#REPLACE는 해보기 REVERSE
#문자열 위치 찾는 4가지 함수 - FIELD / FIND_IN_SET / INSTR / LOCATE

SELECT ELT(2, 'SQL', 'JAVA', 'C');   #헐 위에 글자들 각주로 안했을때도 오류남

SELECT NOW();
SELECT CURDATE();
SELECT CURTIME();

#주석은 문장 끝나고나서!!

select now() 'START', sleep(5), now() as 'END';
select sysdate() 'START', sleep(5), sysdate() as 'END';

use wntrade;


from 고객;

#3-23 데이터엔 없지만 새로운 코드로 만들어야 할 때 if문 사용 많음

SELECT if( (WHERE 단가 = '12500') * 450 > 5000000, '초과달성', '미달성')
FROM 주문세부;

#선생님버전
/*
주문금액 = 단가 * 주문술야
주문금액 >= 5000000 : 초과달성
주문금액 < 5000000 : 미달성
**/

SELECT 주문번호
, 단가
, 주문수량
, 단가* 주문수량 AS 주문금액
, CASE 
	WHEN 단가* 주문수량 >= 5000000 THEN '초과달성'
    WHEN 단가* 주문수량 >= 4000000 THEN '달성'
    ELSE '미달성'
END AS 달성여부
FROM 주문세부;

#등급 부여 A,  부서번호 따라서 부서명 나오게사원부서
#사원 정보 - 부서 번호 대신 부서명
-- --마일리지 등급 부여 VIP, GOLD, SILVER, BRONZE
-- --부서코드 > 부서명으로
-- 마일리지등급

-- select 고객번호, if(마일리지>1000, 'VIP', 'GOLD') as 등급

USE WNTRADE;
SELECT 고객번호
, 마일리지
, CASE
	WHEN 마일리지>= 15000 THEN 'VIP'
    WHEN 7000 <=마일리지 < 15000 THEN 'GOLD'
    WHEN 3000<= 마일리지 < 7000 THEN 'SILVER'
    ELSE 'BRONZE' 
END AS 등급
FROM 고객;

SELECT 부서번호, 부서명
FROM 부서;

SELECT 사원번호, 이름, 부서번호
FROM 사원;

#사원 정보 - 부서 번호 대신 부서명
SELECT 사원번호
, 이름
, CASE
	WHEN 부서번호 = 'A1' THEN '영업부'
    WHEN 부서번호='A2' THEN '기획부'
    WHEN 부서번호='A3' THEN '개발부'
    WHEN 부서번호='A4' THEN '홍보부'
    ELSE '미배정'
END AS 부서명
FROM 사원;

#주문 테이블에 배송상태 추가
#발송일 컬럼 기준, '배송대기', '빠른배송', '일반배송'으로 설정

SELECT 주문번호, 주문일, 요청일, 발송일
FROM 주문;

SELECT 주문번호, 고객번호, 사원번호, 주문일, 요청일, 발송일
, CASE
	WHEN (요청일 - 주문일) <= 14 THEN '빠른배송'
    ELSE '일반배송'
    END AS  배송구분
FROM 주문;


/*연습1. 고객회사명 앞2글자 '*' 마스킹 처리
 * 연습2. 주문세부 정보중 주문금액, 할인금액, 실제주문금액 출력(1단위에서 버림)
 * 연습3. 전체 사원의 이름, 생일, 만나이, 입사일, 입사일수, 입사500일기념일 출력
 * 연습4. 고객 정보의 도시컬럼을 '대도시', '도시'로 구분하고 마일리지 VVIP, VIP, 일반고객 구분
 * 연습5. 주문테이블의 주문일을 주문년도, 분기, 월, 일, 요일, 한글요일로 출력
 * 연습6. 발송일이 요청일보다 7일 이상 늦은 주문건 출력
 * */
 
 SELECT 고객회사명
 FROM 고객;
 
--  --좀이따 하기
--  #연습 1. 고객회사명 앞2글자 *마스킹 처리
-- SELECT 고객번호, 고객회사명, 담당자명, 전화번호
-- REPLACE (고객회사명, 두개 분리 후에


-- 집계함수
select 도시
, count(*)
, count(고객번호)
, count(distinct 도시)
, count( distinct 지역)
, sum(마일리지)
, avg(마일리지)
, min(마일리지)
from 고객
-- where 도시 like '서울%' ;
group by 도시;

-- 집계함수랑 group by 같이 자주 씀

#고객 담당자 이름으로 묶어보기
select 담당자명
, count(고객번호)
from 고객
group by 담당자명;

#고객 담당자 직위로 묶어보기
select 담당자직위
, 도시
, count(고객번호)
, sum(마일리지)
, avg(마일리지)
from 고객
group by 담당자직위, 도시
order by 1,2;



-- Group by  조건 HAVING
-- select
-- from
-- group by
-- having

-- 고객 - 도시별로 그룹 - 고객수, 평균마일리지, 고객수가 -> 10만 추출
select 도시
, COUNT(고객번호) as 고객수
, AVG(마일리지)
from 고객
group by 도시
having count(고객번호)  >= 10;

#고객번호 t로 시작하는 고객을 도시별로 묶어 마일리지 합 출력, 단 1000점 이상만
use wntrade;

select 도시
, sum(마일리지)
from 고객
where 고객번호 like 'T%'
group by 도시
with rollup
having sum(마일리지) >= 1000;

#얘도 고객번호 넣었을 때 안됐음

#광역시 고객, 담당자 직위별로 최대 마일리지, 단, 1만점 이상 레코드만 출력
select 담당자직위
, SUM(마일리지)
, avg(마일리지)
from 고객
where 도시 like '%광역시'
group by 담당자직위
with ROLLUP -- 맨마지막에 총계 행이 추가 
having SUM(마일리지) >= 10000;
#그룹바이에 담당자직위가 있으니까 나올 수  있는데 도시는 어떤 컬럼이 나와야할지 모르니까 나올 수 없다 - 이거 조심!!!!!! 지피티한테 물어보기

#엑셀에서 피벗과 같은 것

#having은 rollup 다음에!! 
select 담당자직위
, SUM(마일리지)
from 고객
where 도시 like '%광역시'
group by 담당자직위
with ROLLUP -- 맨마지막에 총계 행이 추가 
having SUM(마일리지) >= 10000
order by 2 DESC;

-- CROSS JOIN > INNER JOIN
select 부서.부서번호 as 부서부서번호, 사원.부서번호 as 사원부서번호, 이름, 부서명
from 부서 JOIN 사원
on 부서.부서번호 = 사원.부서번호
where 이름 = '배재용';
 
 
 -- 주문, 고객
 select 주문번호, 고객회사명, 주문일
 from 주문 JOIN 고객
where 주문.고객번호 = 'ITCWH';  -- 크로스조인

 select 주문번호, 고객회사명, 주문일
 from 주문 JOIN 고객
 on 주문.고객번호 = 고객.고객번호
where 주문.고객번호 = 'ITCWH'; -- 내부조인 

-- 사원 주문 inner join 주문번호별 담당자
select 주문번호, 이름, 직위, 부서번호
from 주문 JOIN 사원;  -- inner join 안해도 되지 않나? -> 아 사원번호 나타내려고

#선생님버전
select 주문번호, 주문.사원번호, 고객번호, 사원.이름  
from 주문 join 사원
on 주문.사원번호 = 사원.사원번호;
 --  실적 볼 때 
 
 #고객, 제품 > 크로스 조인
 select 고객회사명, 제품명
 from 고객 join 제품; -- 공통 키가 없어서 내부조인 불가 
-- 모든 경우의수 다 보고싶을 때 

--  고객, 마일리지 등급
select 고객.고객회사명, 고객.마일리지, 마일리지등급.등급명
from 고객 join 마일리지등급
on 고객.마일리지 between 마일리지등급.하한마일리지 and 마일리지등급.상한마일리지;
#상한과 하한을 주고 그 안에 있는지 - between
-- 상한마일리지와 하한마일리지가 확정된 값이 아님.. 

-- 크로스조인은 on이 없다 / 내부조인은 두,세개의 테이블을 어떻게 붙일지 조건을 줘야 한다 - on이라는 키워드 
-- 연산자도 사용가능 between, in... 
-- join 연습 많이 하기!! 예제 다 시행해보기!! - 5-3까지  

#5-1 사원테이블, 부서테이블 크로스조인 - 배재용 사원 정보 (이름, 사원 테이블의 부서번호, 부서 테이블의 부서번호, 부서명)
select 이름, 사원.부서번호, 부서.부서번호, 부서명
from 사원 join 부서
where 이름 = '배재용';

#5-2. 이소미 사원의 사원번호, 직위, 부서번호, 부서명 ===> 다시 해보기
select 사원.사원번호
, 직위
, 부서.부서번호
, 부서명
from 사원 join 부서
on 부서.부서번호 = 사원.부서번호
where 이름 = '이소미';

#5-3. 고객 회사들이 주문한 주문건수를 주문건수가 많은 순서대로 보이시오. 
-- 고객번호, 담당자명, 고객회사명 -> 고객주문 고객 고객 
select 고객.고객번호, 담당자명, 고객회사명, count(주문번호)
from 고객 join 주문
on 고객.고객번호 = 주문.고객번호;

select count(주문번호)
from 주문;

#5-3. 고객 회사들이 주문한 주문건수를 주문건수가 많은 순서대로 보이시오. 
-- 고객번호, 담당자명, 고객회사명 -> 고객주문 고객 고객 
select 고객.고객번호
, 담당자명
, 고객회사명
, count(*) as 주문건수
from 고객 join 주문
on 고객.고객번호 = 주문.고객번호
Group by 고객.고객번호, 담당자명, 고객회사명
Order by 주문건수 DESC;

-- ---------------
#테이블 갯수 1개 ->심플 쿼리
#2개 이상 -> 조인
#크로스 조인(카테지안프로덕트 연산) M개 X N개 = MN개 결과를 반환 
#내부 조인(이너조인) 조건에 만족하는 데이터만 반환 - 동등조인, 비동등조인


use WNTRADE;

-- 사원입사일 이후로 처리한 주문 조회 !!!!!!! 얘부터 하기

select 주문번호
, 이름 as 사원명
, 입사일
, 주문일
from 주문 join 사원
on 주문.사원번호 = 사원.사원번호
and 주문.주문일 >= 사원.입사일;

-- 고객회사들이 주문한 건수 집계 > 건수가 많은 순서로 출력

select 고객회사명, 담당자명, 고객.고객번호, count(*) as 주문건수
from 고객 join 주문
on 고객.고객번호 = 주문.고객번호
group by 고객회사명, 담당자명, 고객.고객번호
order by count(*) DESC;

-- 난 맨처음에 select 에 고객번호라고 써서 안됐음
#선생님버전
select 고객.고객번호
, 담당자명
, 고객회사명,
COUNT(*) as 주문건수
from 고객 join 주문
on 고객.고객번호 = 주문.고객번호
group by 고객.고객번호, 담당자명, 고객회사명
order by COUNT(*) desc;

-- 고객회사별 주문금액 합, 큰 금액 순으로 출력 --> 3개 테이블 붙어야됨
select 고객회사명
, 담당자명
, 주문일
, sum(주문수량*단가) as 주문금액

from 고객 JOIN 주문 on 고객.고객번호 = 주문.고객번호
		  JOIN 주문세부 on 주문.주문번호 = 주문세부.주문번호
group by 고객회사명, 담당자명, 주문일
order by 2 DESC;
#sum 할 때 group by 무조건 해야함
# 고객번호로 먼저 연결해야함

select distinct 부서번호
from 부서;

select distinct 부서번호
from 사원;

select 사원번호, 이름, 부서명
from 사원 left join 부서   -- 모든 사원 다 나오게 됨
on 사원.부서번호 = 부서.부서번호;

select 사원번호, 이름, 부서명
from 사원 right join 부서   -- 모든 부서 다 나오게 됨
on 사원.부서번호 = 부서.부서번호;

-- 사원이 없는 부서
select 부서명, 사원번호
from 사원 right join 부서
on 사원.부서번호 = 부서.부서번호
where 사원번호 is null;


-- 부서가 없는 사원

-- 주문 안한 고객

-- 연습１．　담당자　직위에　마케팅이　있는　고객의　담당자직위，　도시별　고객수　출력
-- 단，　담당자직위별　고객수와　전체　고객수도　출력


-- 연습２．　제품　주문년도별　주문건수　출력

-- 연습３．　주문년도，　분기별　주문건수　합계　출력

-- 연습４．　주문　요청일보다　발송이　늦어진　주문내역이　월별로　몇건인지　요약　조회
주문월　순으로　정렬

-- 연습５．　아이스크림　제품별　
