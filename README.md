
## 搭乗数が多い順で並ぶ顧客

```SQL
select 
t.passenger_name,
t.cnt_passenger_name
from 
(
select tickets.passenger_name,count(tickets.passenger_name) as cnt_passenger_name
   from tickets 
where passenger_name is not null
group by passenger_name
order by cnt_passenger_name desc
)t
where
t.cnt_passenger_name > 4000

select tickets.passenger_id,
tickets.passenger_name
from tickets
where passenger_name in
(
'ALEKSANDR IVANOV',
'ALEKSANDR KUZNECOV',
'SERGEY IVANOV',
'SERGEY KUZNECOV',
'VLADIMIR IVANOV'
)

```
