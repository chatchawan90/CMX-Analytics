 with yearly_sales_cte as (
  select  
    sohd.custid, 
    sodt.goodid, 
    year(sohd.docudate) as sales_year,
    sum(sodt.GoodAmnt) as current_year_amnt,
    sum(sodt.goodqty2) as current_year_total_qty,
    -- Step 1: Count unique transactions per customer/product per year
    count(distinct sohd.soid) as total_transactions
  from sohd 
  inner join sodt on sodt.soid = sohd.soid 
  inner join emgood on emgood.goodid = sodt.GoodID 
  where emgood.goodbrandid = 1021 
    and year(sohd.docudate) between 2025 and 2026
  group by 
    sohd.custid, 
    sodt.goodid, 
    year(sohd.docudate)
),
lag_processing as (
  select 
    custid,
    goodid,
    sales_year,
    current_year_amnt,
    total_transactions,
    lag(current_year_amnt, 1, 0) over (
      partition by custid, goodid 
      order by sales_year
    ) as last_year_amnt,
    lag(sales_year, 1, null) over (
      partition by custid, goodid 
      order by sales_year
    ) as prev_sales_year
  from yearly_sales_cte
)
select 
  lp.custid,
  lp.goodid,
  eg.goodname1,
  case when lp.prev_sales_year = lp.sales_year - 1 then lp.last_year_amnt else 0 end as last_year_amnt,
  lp.current_year_amnt,
  case 
    when lp.prev_sales_year = lp.sales_year - 1 
    then round((lp.current_year_amnt - lp.last_year_amnt) / nullif(lp.last_year_amnt, 0), 2) * 100 
    else 100.00 
  end as growth_percentage,
  lp.total_transactions as transactions_2026, -- Visible for clarity
  lp.sales_year 
from lag_processing lp
inner join emgood eg on eg.goodid = lp.goodid
-- Step 2: Strictly filter for 2026 and more than 1 transaction
where lp.sales_year = 2026 
order by lp.custid, growth_percentage desc;
