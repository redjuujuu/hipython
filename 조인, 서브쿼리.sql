SELECT 제품명 
, 단가
, 재고 AS "구매 가능 수량!!" -- * 
, 단가*재고 AS ""

FROM 제품;


SELECT * FROM wntrade.고객;
use wntrade;
show tables;

SELECT 사원번호, 이름, 부서명
FROM 사원 LEFT JOIN 부서
ON 사원.부서번호 = 부서.부서번호;

SELECT  A.고객회사명, A.담당자명, A.마일리지
FROM 고객 A
LEFT JOIN 고객 B
ON A.마일리지 < B.마일리지
WHERE B.고객번호 IS NULL;

use wntrade;

SELECT  A.고객회사명, A.담당자명, A.마일리지, B.고객회사명, B.마일리지
FROM 고객 as A
LEFT JOIN 고객 as B -- 셀프조인
ON A.마일리지 < B.마일리지 -- a의 마일리지 < b.마일리지
-- where B.고객번호 IS NULL
order by A.마일리지 desc;
# 똑같은 애를 복사해서, 이름을 A, B로 한 것임

select distinct 부서번호
from 사원;

select COUNT(*)
from 부서;

select 사원번호, 이름, 부서명
from 사원 left join 부서
on 사원.부서번호 = 부서.부서번호;

--사원이 없는 부서
--주문  안한 고객

select 고객회사명, 고객.고객번호
from 고객 join 주문
on 고객.고객번호 = 주문.고객번호
where 고객회사명='인터비스';

use wntrade;
select 고객번호
	,고객회사명
    ,담당자명
    ,마일리지
    ,등급명
from 고객
inner join 마일리지등급
on 마일리지 >= 하한마일리지
and 마일리지 <= 상한마일리지
where 담당자명 = '이은광';

select 고객번호
	,고객회사명
    ,담당자명
    ,마일리지
    ,등급명
from 고객
inner join 마일리지등급
on 고객.마일리지 between 마일리지등급.하한마일리지 and 마일리지등급.상한마일리지
where 담당자명 = '이은광';

use wntrade;

#--부서가 없는 사원까지 보는 쿼리
select 사원번호, 이름, 부서명
from 사원 left join 부서    #(여기서 왜 부서명이 아니라 부서야?)
on 사원.부서번호 = 부서.부서번호;


#--사원이 없는 부서 - 부서기준으로
select 부서명
	,사원.*
from 사원 right join 부서 
on 사원.부서번호 = 부서.부서번호
where 사원.부서번호 IS NUll;

-- 주문 안한 고객
#주문이 없는 고객까지 들고와야 하니까 외부조인..?
select 고객.고객회사명, 고객.담당자명
from 고객 left join 주문
on 고객.고객번호 = 주문.고객번호   # outer 
where 주문.주문번호 is null;
#기준테이블이 왼쪽
#주문번호 없는 애..

-- 셀프 조인
-- 사원별 상사의 이름
select 사원.이름, 상사.이름
from 사원 left join 사원 as 상사
on 사원.상사번호 = 상사.사원번호
where 사원.상사번호 ='';  #(is null로 할 때는 왜 안됐고, ''로하니까 왜 되는거야?)
#(사원의 상사를 알고싶으니까)


-- 서브쿼리
use wntrade;

select 고객번호, 마일리지
from 고객
where 마일리지 = (
	select MAX(마일리지)
	from 고객
); -- 최고 마일리지 값

use wntrade;
select max(마일리지)
		from 고객;

# 6-2
select 고객.고객회사명, 고객.담당자명
from 고객 join 주문 on 고객.고객번호 = 주문.고객번호
-- (양쪽에 다 ㅣㅇㅆ는 경우만 들고오면 되니까 내부조인하면됨)
where 주문번호 = 'h0250' ;

-- subquery version (내버전)
select 고객.고객회사명, 고객.담당자명
from 고객
where 고객.고객번호 = ( 
	select 고객번호 = 'h0250' 
    from 주문 ); -- 주문번호='h0250' 고객
    
-- 선생님버전

select 주문.고객번호
from 주문
where 주문.주문번호 = 'h0250';

select 고객.고객회사명, 고객.담당자명
from 고객
where 고객.고객번호 = ( 
	select 주문.고객번호
	from 주문
	where 주문.주문번호 = 'h0250' );
    
# 6-3
-- 부산광역시 고객의 최소 마일리지보다 더 큰 마일리지 가진 고객정보
#(내 버전 - join을 사용하려고 함)
select 고객.*, 마이
from 고객 join 고객 as 마일리지
where 마일리지 = Min(마일리지)

#선생님 버전
use wntrade;

select 고객회사명, 마일리지
from 고객
where 고객.마일리지 > (
select min(마일리지) 
from 고객
where 고객.도시 = '부산광역시'
); -- 서브쿼리

use wntrade;
select min(마일리지) 
from 고객
where 고객.도시 = '부산광역시';
    
#6-4
-- 부산광역시 고객의 주문건수
select count(*)
from 주문
where 고객번호 in (
	select 고객번호   -- 앞에 고객번호가 있으니까 select뒤에도 고객번호 형식이 와야함
    from 고객
    where 도시 = '부산광역시'
    );
 
 #6-5 (any / all / exist)
 -- any
select 담당자명
, 고객회사명
,마일리지
,도시
from 고객
where 마일리지 > ANY (select 마일리지
						from 고객
                        where 도시 = '부산광역시'
                        );  #[5건 후보 중에 최솟값보다 크면 됨]
           

-- all         
use wntrade;
select 담당자명, 고객회사명, 마일리지, 도시
from 고객
where 마일리지 > all (select 마일리지 
					from 고객
                    where 도시 = '부산광역시'
                    );  -- all 이 and라서 any가 더 큼
                    

-- exist (비교연산자가 아니라 존재하는지 아닌지)
select 담당자명, 고객회사명, 마일리지
from 고객 a
where exists (
	select 1
    from 고객 b
    where 도시 = '부산광역시' and a.마일리지 > b. 마일리지
); 
# 반드시 a, b  앨리어스? 

#6-8
#그룹의 조건 > Having의 조건절 서브쿼리

select 도시, AVG(마일리지) AS 평균마일리지, (Select Avg(마일리지) From 고객) as 전체평균마일리지   -- 이게 전체 평균이 아닌건가?
FROM 고객
GROUP BY 도시 -- 아 도시로 묶어서 괜찮은거?? 여기서 고객.도시 안해도돼?
Having Avg(마일리지) > (Select Avg(마일리지)
							From 고객
                            );

####전체 평균이 얼마인지도 표현하고 싶다 -> 스칼라 사용하면 됨

#6-9
#from에 들어가는 가상테이블 > 인라인뷰
-- 담당자명, 고객회사명, 마일리지, 도시, 해당 도시의 평균마일리지, 갭
-- 도시의 평균마일리지 구해서 join 하면 심플함....
-- 이퀴조인을 걸어줘야 빠르잖아.. 
select 담당자명
	, 고객회사명
	, 마일리지
	, 고객.도시    -- 선생님이 그냥 도시라고 썼었는데 모호하다고 해서 더 명확하게함
	, 도시_평균마일리지
	, 도시_평균마일리지 - 마일리지 AS 차이

FROM 고객
	,(Select 도시
			,AVG(마일리지) AS 도시_평균마일리지
	 From 고객
     Group by 도시
     ) AS 도시별요약
where 고객.도시 = 도시별요약.도시
order by 차이 desc;

#6-10 
# 칼럼 목록에 들어가는 > 스칼라 서브쿼리

select 고객번호  -- 여기서 고객.고객번호 안해도 되는구나
, 담당자명
, (Select Max(주문일)
	FROM 주문
    WHERE 주문.고객번호 = 고객.고객번호
    ) AS 최종주문일                        -- 얘네를 잘 모르겠음
FROM 고객;