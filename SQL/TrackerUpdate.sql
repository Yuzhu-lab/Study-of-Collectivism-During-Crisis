create table masterdatabase (HHIDPN float, Coll_Index smallint, Which_Year_Answer smallint, Income float); 
select * from masterdatabase;

create table Tracker_Across_Wave (HHIDPN FLOAT,HHID INTEGER, PN Smallint, degree smallint, gender smallint, race smallint, hispanic smallint, usborn smallint, yrenter integer, race_dominate smallint);

select A.HHIDPN, A.coll_index, A.which_year_answer, A.income, B.degree, B.gender, B.usborn, B.yrenter,B.race_dominate   
into new_master_database
from masterdatabase as A
inner join tracker_across_wave as B
on A.HHIDPN = B.HHIDPN
where yrenter>=1998
order by HHIDPN, which_year_answer;

select * from new_master_database;
