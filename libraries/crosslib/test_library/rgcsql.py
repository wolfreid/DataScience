
query = dict()
query_coll = dict()


def get_query(query_coll,code):
    
    return query_coll[code]

query["oper_volumes"] = \
            '''SELECT
            DATEADD(DAY,CAST(DATEPART(DAY,T1._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,T1._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,T1._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
            T2._Fld11959RRef,
            T3._Fld11762RRef,
            T2._Fld11961RRef,
            CAST(SUM(T1._Fld11928) AS NUMERIC(24,  8)) as 'Рассход',

            T3._Fld11762RRef,
            T4._Description,
            T2._Fld11959RRef,
            T5._Description,
            T2._Fld11961RRef,
            T6._Description,
            T6._Code
            FROM dbo._AccumRg11926 T1
            LEFT OUTER JOIN dbo._Reference11902 T2
            ON T1._Fld11927RRef = T2._IDRRef
            LEFT OUTER JOIN dbo._Reference37 T3
            ON T2._Fld11966RRef = T3._IDRRef
            LEFT OUTER JOIN dbo._Reference11759 T4
            ON T3._Fld11762RRef = T4._IDRRef
            LEFT OUTER JOIN dbo._Reference70 T5
            ON T2._Fld11959RRef = T5._IDRRef
            LEFT OUTER JOIN dbo._Reference7604 T6
            ON T2._Fld11961RRef = T6._IDRRef

            WHERE (T1._Period >= '4021-11-01') AND (T1._Period <= '4021-11-10') --AND (T1._Fld11928 <> 0) AND (T2._Fld12968RRef = 0x9733E3D43C27FEA647D500D6948D39E1)
            GROUP BY DATEADD(DAY,CAST(DATEPART(DAY,T1._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,T1._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,T1._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))),
            T2._Fld11959RRef,
            T3._Fld11762RRef,
            T2._Fld11961RRef,
            T3._Fld11762RRef,
            T4._Description,
            T2._Fld11959RRef,
            T5._Description,
            T2._Fld11961RRef,
            T6._Description,
            T6._Code'''    

query["sectors_short"] = \
    '''select o._Code as "ВОГ_Код",o._Description as "ВОГ",
        s._Code as "Сектор_получатель_Код", s._Description as "Сектор_получатель_Код",q._Code as "ГРС_Код",q._Description as "ГРС"  from _Reference9673 o	
        inner join  dbo._Reference7604 s on o.[_Fld9682_RRRef] = s.[_IDRRef]
        inner join dbo._Reference7594 q on o.[_Fld9678RRef] = q.[_IDRRef]
        order by o._Description, s._Description'''

query["sectors_full"] = \
            '''select ORG._Description as "Організація", Code2 as "Сектор.Код.Ознака",Desc2 as "Сектор.Ознака",
        isnull(final.Code1, final.Code2) as "Сектор.Код", isnull(final.Desc1, final.Desc2) as "Сектор",
        (case 
            when isnull(final.Code1, final.Code2) = Code2 then 'Батьківський елемент'
            else 'Дочірній елемент' end) as "Тип" from  
        (SELECT T1._Fld7725RRef,T1._Code as Code1, T1._Description as Desc1,T2._Code as Code2, T2._Description  as Desc2 FROM _Reference7604 T1
        inner join _Reference7604 T2
        on T1._IDRRef = T2._ParentIDRRef
        --order by T1._Description
        union
        sELECT T4._Fld7725RRef,T3._Code as Code1, T3._Description as Desc1,T4._Code as Code2, T4._Description as Desc2 FROM _Reference7604 T3
        right join _Reference7604 T4
        on T3._IDRRef = T4._ParentIDRRef
        where T3._Code is null) as final

        inner join _Reference70 as ORG
        on final._Fld7725RRef = ORG._IDRRef''' 
query["VOG_Sectors_GRS"] = \
        '''select * from 
        (select o._Code as VOG_code,o._Description as VOG,
        s._Code as Sector_Code, s._Description as Sector,
        q._Code as GRS_Code,q._Description as GRS, 'Сектор обліку' as "Тип сектору"   from _Reference9673 o	
        inner join  dbo._Reference7604 s on o.[_Fld9682_RRRef] = s.[_IDRRef]
        inner join dbo._Reference7594 q on o.[_Fld9678RRef] = q.[_IDRRef]
        --order by o._Description, s._Description
        union all
        select o._Code as "ВОГ_Код",o._Description as "ВОГ",
        s._Code as "Сектор_получатель_Код", s._Description as "Сектор_получатель_Код",
        q._Code as "ГРС_Код",q._Description as "ГРС",'Сектор алгоритм' as "Тип сектору"  from _Reference9673 o	
        inner join  dbo._Reference7604 s on o.[_Fld9681_RRRef] = s.[_IDRRef]
        inner join dbo._Reference7594 q on o.[_Fld9678RRef] = q.[_IDRRef]) as final
        order by final.Sector '''
query['oper_volumes_expand']= \
    '''
            SELECT
            T5._Description as 'Организация',
            DATEADD(DAY,CAST(DATEPART(DAY,T1._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,T1._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,T1._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
            --T2._Fld11959RRef,
            --T3._Fld11762RRef,
            --T2._Fld11961RRef,
            --T3._Fld11762RRef,
            Case when T4._Description='ВТВ' or T4._Description='Населення' then 'Населення+ВТВ' --if T6._Description=T6._Description
                when T4._Description='Промисловість' then 'Промисловість'
                when T4._Description='Бюджет' then 'Бюджет'
                when T4._Description='Релігія' then 'Релігія'
                when T4._Description='Теплоенергетика' then 'Теплоенергетика'
                when T4._Description='Власні потреби' then 'Власні потреби'
            end as 'Категория',
            --T4._Description as 'Категория потребителя',
            --T2._Fld11959RRef,
            --T2._Fld11961RRef,
            T6._Description as 'Сектор',
            --T6._Code
            CAST(SUM(T1._Fld11928) AS NUMERIC(24, 8))as 'Расход'

            FROM dbo._AccumRg11926 T1
            LEFT OUTER JOIN dbo._Reference11902 T2
            ON T1._Fld11927RRef = T2._IDRRef
            LEFT OUTER JOIN dbo._Reference37 T3
            ON T2._Fld11966RRef = T3._IDRRef
            LEFT OUTER JOIN dbo._Reference11759 T4
            ON T3._Fld11762RRef = T4._IDRRef
            LEFT OUTER JOIN dbo._Reference70 T5
            ON T2._Fld11959RRef = T5._IDRRef
            LEFT OUTER JOIN dbo._Reference7604 T6
            ON T2._Fld11961RRef = T6._IDRRef

            WHERE (T1._Period >= '4021-11-01') AND (T1._Period <= '4021-11-10') AND (T1._Fld11928 <> 0) AND (T2._Fld12968RRef = 0xAE03BC3AF00BFC864D611FC70FB6C96C)
            GROUP BY DATEADD(DAY,CAST(DATEPART(DAY,T1._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,T1._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,T1._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))),
            --T2._Fld11959RRef,
            --T3._Fld11762RRef,
            --T2._Fld11961RRef,
            --T3._Fld11762RRef,
            Case when T4._Description='ВТВ' or T4._Description='Населення' then 'Населення+ВТВ' 
                when T4._Description='Промисловість' then 'Промисловість'
                when T4._Description='Бюджет' then 'Бюджет'
                when T4._Description='Релігія' then 'Релігія'
                when T4._Description='Теплоенергетика' then 'Теплоенергетика'
                when T4._Description='Власні потреби' then 'Власні потреби'
            end,
            --T4._Description,
            --T2._Fld11959RRef,
            T5._Description,
            --T2._Fld11961RRef,
            T6._Description
            --T6._Code
            order by T5._Description, T6._Description, 2'''


query['fact_volumes']= \
        '''SELECT top(10)
        DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
        s._Code as 'Сектор_Код',
        t._Code as 'Точка учета_Код ',
        p._Description,
        CAST(SUM(f._Fld11547) AS NUMERIC(24, 8)) as 'Факт Расход'

        --FROM dbo._AccumRg12072 f --Индексы ОперативныеРасходыСекторов
        FROM dbo._AccumRg11545 f
        --LEFT OUTER JOIN dbo._Reference12057 r ---ИзмеренияРегистра_ФактическиеРасходыСекторов
        LEFT OUTER JOIN dbo._Reference11544 r --ИзмеренияРегистра_СуточныеРасходыСекторов
        --ON f._Fld12073RRef = r._IDRRef
        ON f._Fld11546RRef = r._IDRRef
        LEFT OUTER JOIN dbo._Reference37 c --ДоговорыКонтрагентов
        ON r._Fld11563RRef = c._IDRRef
        LEFT OUTER JOIN dbo._Reference11759 p --КатегорииПотребителей
        ON c._Fld11762RRef = p._IDRRef
        LEFT OUTER JOIN dbo._Reference70 o --Организации
        ON r._Fld11558RRef = o._IDRRef
        LEFT OUTER JOIN dbo._Reference7600 t --ТочкиУчета
        ON r._Fld11564RRef = t._IDRRef
        LEFT OUTER JOIN dbo._Reference7604 s --Секторы
        ON r._Fld11899RRef = s._IDRRef


        WHERE f._Period between  '4021-10-01' and '4021-10-31' AND (f._Fld11547 <> 0) --AND (r._Fld12104 = 0xAE03BC3AF00BFC864D611FC70FB6C96C) 
        and p._Description not like 'ВТВ' and p._Description not like 'Населення'  --and t._Code='ВІ0000132' --and p._Description like 'Релігія' --and t._Code is null
        GROUP BY 
        DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))),
        s._Code,p._Description, t._Code

        order by t._Code, DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'})))'''


query['points_contragent']= \
        '''        -----------!!!!!!!!Справочник контрагентов!!!!!!!!!!!
        use IndCons
        go
        select distinct
            s._Description as 'Сектор', s._Code as 'Сектор_код', contr._Description as 'Контрагент', 
            contr._Code as 'Контрагент_код'--, p._Description as 'Категория потребителя'
        order by s._Description
        from dbo._Reference11544 r --ИзмеренияРегистра_СуточныеРасходыСекторов
        LEFT OUTER JOIN dbo._Reference59 contr on r._Fld11562RRef = contr._IDRRef--Справочник контрагентов
        LEFT OUTER JOIN dbo._Reference7604 s ON r._Fld11899RRef = s._IDRRef--Секторы'''

query['sectors_switchers'] = \
        '''select o._Description as 'ПАТ', o._Code, o._Fld10448 as 'ПАТ_код',
        s._Description as 'Сектор', s._Code as 'Сектор_код', p._Description as 'Перемычка', --a._Document10116_IDRRef, t._IDRRef,--a._Fld10356RRef as 'Статус премычки'
        DATEADD(DAY,CAST(DATEPART(DAY,t._Date_Time) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,t._Date_Time) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,t._Date_Time) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
        case a._Fld10356RRef
        when 0x88E038355C1324174CEB2EABF2D57CAD then 'Открыта' 
        when 0x9E732555E68660044CC287C97EC6D996 then 'Закрыта' 
        when 0x82372952E88A82694AABCCB8A01491DD then 'Ликвидировано' 
        end as 'Статус премычки'

        from dbo._Reference70 o --Справочник Организаций
        left join  dbo._Reference7604 s on o.[_IDRRef]=s.[_Fld7725RRef] --Справочник Секторов
        left join dbo._Reference10115 p on s._IDRRef=p._Fld10156RRef or s._IDRRef=p._Fld10157RRef --Справочник Перемычек
        left join dbo._Document10116_VT10353 a on p._IDRRef=a._Fld10355RRef --СТАТУС Перемычек
        left join dbo._Document10116 t on a._Document10116_IDRRef=t._IDRRef --Регистр изменений СТАТУСа Перемычек

        /*where t._Date_Time =(select max(_Date_Time) from  dbo._Reference10115 p -- фильтрация статуса перемычки по мах дате
        left join dbo._Document10116_VT10353 aa on p._IDRRef=aa._Fld10355RRef and a._Fld10355RRef=aa._Fld10355RRef
        left join dbo._Document10116 t on aa._Document10116_IDRRef=t._IDRRef
        )*/

        order by o._Description, s._Description, t._Date_Time'''

query['category-consuming']  = \
    '''select distinct 
       contr._Description as 'Контрагент', 
	   contr._Code as 'Контрагент_код', p._Description as 'Категория потребителя',o._Description as 'Галузь'

from dbo._Reference11544 r --ИзмеренияРегистра_СуточныеРасходыСекторов
LEFT OUTER JOIN dbo._Reference37 c ON r._Fld11563RRef = c._IDRRef --ДоговорыКонтрагентов
LEFT OUTER JOIN dbo._Reference59 contr on r._Fld11562RRef = contr._IDRRef--Справочник контрагентов
LEFT OUTER JOIN dbo._Reference11759 p ON c._Fld11762RRef = p._IDRRef --КатегорииПотребителей
left outer join dbo._Reference7605 o on contr._Fld9488RRef= o._IDRRef 

order by p._Description'''

query["points"] = \
    '''select distinct
        n._Code as "Cектор обліку.Код",
       contr._Description as 'Контрагент', 
	   contr._Code as 'Контрагент_код', t._Description as 'Точка учета', t._Code as 'Точка учета_код', 
	   case t._Fld11539  
	        when 0x00 then 0
			when 0x01 then 1 end as 'Группа риска'
from dbo._Reference11544 r --ИзмеренияРегистра_СуточныеРасходыСекторов
LEFT OUTER JOIN dbo._Reference59 contr on r._Fld11562RRef = contr._IDRRef--Справочник контрагентов
LEFT OUTER JOIN dbo._Reference7600 t ON r._Fld11564RRef = t._IDRRef --ТочкиУчета
left outer join dbo._Reference7604 n on n._IDRRef = t._Fld7701RRef

order by  contr._Description'''

query["sectors_short"] = \
    '''select 
o._Description as 'ПАТ', s._Description as 'Сектор', s._Code as 'Сектор_код', n._Description as 'Подсектор', n._Code as 'ПодСектор_код'
from dbo._Reference7604 s
left join dbo._Reference7604 n on s._IDRRef=n._ParentIDRRef
left join dbo._Reference70 o on  o._IDRRef=s._Fld7725RRef
where s._ParentIDRRef=0x00000000000000000000000000000000
order by o._Description, s._Description'''

query["route_light"] = \
    '''
    select top(20) t2._Active,t3._Code as 'Сектор.Код',t3._Description as 'Сектор',t2._Period as 'Зміна',t1._Code as 'Маршрут.Код',t1._Description as 'Маршрут'from _Reference10668 t1 --маршруты
    left join _InfoRg10876 t2 on t1._IDRRef= t2._Fld10880RRef -- изменения
    left join _Reference7604 t3 on t3._IDRRef = t2._Fld10879RRef --Сектора
    '''
query["route"] = \
     '''
    select /*top(15) distinct*/ md._Description as 'Маршрут', md._Code as 'Маршрут_код',  s._Description as 'Сектор', s._Code as 'Сектор_код', 
    --s._Fld11144RRef,
    case s._Fld11144RRef
    when 0xab28e5aec825b76f474412835e57d809 then 'Прямая Труба'
    when 0xb2395570635b15dd49ce50f163ecdc80 then 'Тупик'
    when 0x8fc082c343e6135e4e5193263697ce06 then 'Кольцо'
    when 0x8950625b082148684b41629fde0412d1 then 'Перемычка'
    when 0xb0d6d829c7a23f9f474e31c960882283 then 'Перемычка/Кольцо'  
    when 0x00000000000000000000000000000000 then 'Перемычка'
    end as'Статус ГРС',
    DATEADD(DAY,CAST(DATEPART(DAY,m._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,m._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,m._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'})))as 'Дата', 
    case md._Fld10888
    when 0x01 then 1
    when 0x00 then 0 end as 'Актуальность',
    case md._Fld10883RRef
    when 0x950ba2c1b045729443106ae972aea647 then 'Магистральный'
    when 0xAD2E93D77116074241696A8F6E54B809 then 'Внутренний'
    when 0x901DE5E4B22B19824EAE4EA73EECBB4A then 'Смешанный'
    when 0xb44274a1506bb2d24beae7b7e9570156 then 'Собственный' end as 'Тип Маршрута'
    from dbo._InfoRg10876 m
    left join dbo._Reference10668 md on m._Fld10880RRef=md._IDRRef
    left join dbo._Reference7604 s on m._Fld10879RRef=s._IDRRef
    where s._ParentIDRRef = 0x00000000000000000000000000000000 --and s._Fld11144RRef = 0x00000000000000000000000000000000
    '''   
query["energy_oper_point"] = \
    '''SELECT
    DATEADD(DAY,CAST(DATEPART(DAY,T1._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,T1._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,T1._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
    T7._Code as 'Сектор.Код',
    CAST(SUM(T1._Fld11930) AS NUMERIC(24, 8))as 'Витрата.Енергія',
    t4._Description as 'Категорія споживача', 2 as 'Тип звіту'

    FROM dbo._AccumRg11926 T1 --Регистры Накопления ОперативныеРасходыСекторов
    LEFT OUTER JOIN dbo._Reference11902 T2 ---ИзмеренияРегистра_ОперативныеРасходыСекторов
    ON T1._Fld11927RRef = T2._IDRRef
    LEFT OUTER JOIN dbo._Reference37 T3 --ДоговорыКонтрагентов
    ON T2._Fld11966RRef = T3._IDRRef
    LEFT OUTER JOIN dbo._Reference11759 T4 --КатегорииПотребителей
    ON T3._Fld11762RRef = T4._IDRRef
    LEFT OUTER JOIN dbo._Reference70 T5 --Организации
    ON T2._Fld11959RRef = T5._IDRRef
    LEFT OUTER JOIN dbo._Reference7600 T6 --ТочкиУчета
    ON T2._Fld11967RRef = T6._IDRRef
    LEFT OUTER JOIN dbo._Reference7604 T7 --Секторы
    ON T2._Fld11961RRef = T7._IDRRef

    WHERE 
    T1._Period >=iif(day(getdate())>=9,
                datefromparts(year(getdate())+2000,month(getdate()),01), 
                    iif(day(getdate())<9 and month(getdate())=1,
                    datefromparts(datepart(yyyy,dateadd(yy,-1,Convert(DateTime, Convert(DateTime,getdate(),104))))+2000,datepart(mm,dateadd(m,-1,Convert(DateTime, Convert(DateTime,getdate(),104)))),01),
                    datefromparts(year(getdate())+2000,datepart(mm,dateadd(m,-1,Convert(DateTime, Convert(DateTime,getdate(),104)))),01)))
    AND (T1._Fld11928 <> 0) AND (T2._Fld12968RRef = 0xAE03BC3AF00BFC864D611FC70FB6C96C /*Расчет по D-1*/) 
    and T4._Description not like 'ВТВ' and T4._Description not like 'Населення'
    GROUP BY
    DATEADD(DAY,CAST(DATEPART(DAY,T1._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,T1._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,T1._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))), T7._Code,t4._Description

    order by  DATEADD(DAY,CAST(DATEPART(DAY,T1._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,T1._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,T1._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'})))
    '''
query["energy_fact_coming_sector"] = \
    '''select 
        DATEADD(DAY,CAST(DATEPART(DAY,r._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,r._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,r._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
        s._Code as 'Сектор код',
        CAST(SUM(r._Fld11882) AS NUMERIC(24, 8)) as 'Поступление Факт',1 as 'Тип звіту' 
        from dbo._AccumRg11880 r
        left join dbo._Reference11879 i on r._Fld11881RRef=i._IDRRef
        left join dbo._Reference70 o on o._IDRRef=i._Fld11893RRef
        left join dbo._Reference7604 s on s._IDRRef=i._Fld11895RRef

        WHERE r._Period between  '4019-01-01' and '4021-11-30'

        group by DATEADD(DAY,CAST(DATEPART(DAY,r._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,r._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,r._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))),
        s._Code
        order by s._Code,
        DATEADD(DAY,CAST(DATEPART(DAY,r._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,r._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,r._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'})))'''

query["energy_fact_point"]  =\
    '''SELECT
    DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
    t._Code as 'Точка обліку.Код ',
    CAST(SUM(f._Fld11548) AS NUMERIC(24, 8)) as 'Витрата.Енергія',  
    p._Description as 'Категорія споживача', 1 as 'Тип звіту'    

    FROM dbo._AccumRg11545 f
    LEFT OUTER JOIN dbo._Reference11544 r --ИзмеренияРегистра_СуточныеРасходыСекторов
    ON f._Fld11546RRef = r._IDRRef
    LEFT OUTER JOIN dbo._Reference37 c --ДоговорыКонтрагентов
    ON r._Fld11563RRef = c._IDRRef
    LEFT OUTER JOIN dbo._Reference11759 p --КатегорииПотребителей
    ON c._Fld11762RRef = p._IDRRef
    left join dbo._Reference7605 aa on c._Fld9487RRef=aa._IDRRef
    LEFT OUTER JOIN dbo._Reference70 o --Организации
    ON r._Fld11558RRef = o._IDRRef
    LEFT OUTER JOIN dbo._Reference7600 t --ТочкиУчета
    ON r._Fld11564RRef = t._IDRRef
    LEFT OUTER JOIN dbo._Reference7604 s --Секторы
    ON r._Fld11899RRef = s._IDRRef


    WHERE f._Period between  '4021-01-01' and '4021-11-30' AND (f._Fld11547 <> 0)
    and p._Description not like 'ВТВ' and p._Description not like 'Населення'

    GROUP BY 
    DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))),
    s._Code,p._Description, t._Code, aa._Description, p._Description 

    order by t._Code, DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'})))

    '''  

query["energy_oper_coming_sector"]  = \
        '''SELECT
    DATEADD(DAY,CAST(DATEPART(DAY,T1._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,T1._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,T1._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
    T7._Code as 'Сектор.Код',
    T6._Code as 'Точка обліку.Код ',
    CAST(SUM(T1._Fld11930) AS NUMERIC(24, 8))as 'Витрата.Енергія',
    t4._Description as 'Категорія споживача', 2 as 'Тип звіту'

    FROM dbo._AccumRg11926 T1 --Регистры Накопления ОперативныеРасходыСекторов
    LEFT OUTER JOIN dbo._Reference11902 T2 ---ИзмеренияРегистра_ОперативныеРасходыСекторов
    ON T1._Fld11927RRef = T2._IDRRef
    LEFT OUTER JOIN dbo._Reference37 T3 --ДоговорыКонтрагентов
    ON T2._Fld11966RRef = T3._IDRRef
    LEFT OUTER JOIN dbo._Reference11759 T4 --КатегорииПотребителей
    ON T3._Fld11762RRef = T4._IDRRef
    LEFT OUTER JOIN dbo._Reference70 T5 --Организации
    ON T2._Fld11959RRef = T5._IDRRef
    LEFT OUTER JOIN dbo._Reference7600 T6 --ТочкиУчета
    ON T2._Fld11967RRef = T6._IDRRef
    LEFT OUTER JOIN dbo._Reference7604 T7 --Секторы
    ON T2._Fld11961RRef = T7._IDRRef

    WHERE 
    T1._Period >=iif(day(getdate())>=9,
                datefromparts(year(getdate())+2000,month(getdate()),01), 
                    iif(day(getdate())<9 and month(getdate())=1,
                    datefromparts(datepart(yyyy,dateadd(yy,-1,Convert(DateTime, Convert(DateTime,getdate(),104))))+2000,datepart(mm,dateadd(m,-1,Convert(DateTime, Convert(DateTime,getdate(),104)))),01),
                    datefromparts(year(getdate())+2000,datepart(mm,dateadd(m,-1,Convert(DateTime, Convert(DateTime,getdate(),104)))),01)))
    AND (T1._Fld11928 <> 0) AND (T2._Fld12968RRef = 0xAE03BC3AF00BFC864D611FC70FB6C96C /*Расчет по D-1*/) 
    and T4._Description not like 'ВТВ' and T4._Description not like 'Населення'
    GROUP BY
    DATEADD(DAY,CAST(DATEPART(DAY,T1._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,T1._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,T1._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))),
    T6._Code, T7._Code,t4._Description

    order by T6._Code, DATEADD(DAY,CAST(DATEPART(DAY,T1._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,T1._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,T1._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'})))

    '''

query["energy_oper_coming_sector"] = \
    '''select 
        DATEADD(DAY,CAST(DATEPART(DAY,r._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,r._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,r._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
        s._Code as 'Сектор код',
        CAST(SUM(r._Fld11916) AS NUMERIC(24, 8)) as 'Поступление опер', 2 as 'Тип звіту'
        --,CAST(SUM(r._Fld11917) AS NUMERIC(24, 8)) as 'Поступление опер'  
        from dbo._AccumRg11914 r
        left join dbo._Reference11901 i on r._Fld11915RRef=i._IDRRef
        left join dbo._Reference70 o on o._IDRRef=i._Fld11954RRef
        left join dbo._Reference7604 s on s._IDRRef=i._Fld11956RRef

        WHERE r._Period >=iif(day(getdate())>=9,
                    datefromparts(year(getdate())+2000,month(getdate()),01), 
                        iif(day(getdate())<9 and month(getdate())=1,
                        datefromparts(datepart(yyyy,dateadd(yy,-1,Convert(DateTime, Convert(DateTime,getdate(),104))))+2000,datepart(mm,dateadd(m,-1,Convert(DateTime, Convert(DateTime,getdate(),104)))),01),
                        datefromparts(year(getdate())+2000,datepart(mm,dateadd(m,-1,Convert(DateTime, Convert(DateTime,getdate(),104)))),01)))

        group by DATEADD(DAY,CAST(DATEPART(DAY,r._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,r._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,r._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))),
        s._Code
        order by s._Code,
        DATEADD(DAY,CAST(DATEPART(DAY,r._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,r._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,r._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'})))'''
    
query["energy_fact_consuming_sector"]  = \
    '''SELECT
        DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
        s._Code as 'Сектор.Код',
        CAST(SUM(f._Fld11547) AS NUMERIC(24, 8)) as 'Витрата' ,
        CAST(SUM(f._Fld11548) AS NUMERIC(24, 8)) as 'Витрата.Енергія',  
        p._Description as 'Категорія споживача', 1 as 'Тип звіту'    

        FROM dbo._AccumRg11545 f
        LEFT OUTER JOIN dbo._Reference11544 r --ИзмеренияРегистра_СуточныеРасходыСекторов
        ON f._Fld11546RRef = r._IDRRef
        LEFT OUTER JOIN dbo._Reference37 c --ДоговорыКонтрагентов
        ON r._Fld11563RRef = c._IDRRef
        LEFT OUTER JOIN dbo._Reference11759 p --КатегорииПотребителей
        ON c._Fld11762RRef = p._IDRRef
        left join dbo._Reference7605 aa on c._Fld9487RRef=aa._IDRRef
        LEFT OUTER JOIN dbo._Reference70 o --Организации
        ON r._Fld11558RRef = o._IDRRef
        LEFT OUTER JOIN dbo._Reference7600 t --ТочкиУчета
        ON r._Fld11564RRef = t._IDRRef
        LEFT OUTER JOIN dbo._Reference7604 s --Секторы
        ON r._Fld11899RRef = s._IDRRef


        WHERE f._Period between  '4021-01-01' and '4021-11-30' AND (f._Fld11547 <> 0)
        and p._Description not like 'ВТВ' and p._Description not like 'Населення'

        GROUP BY 
        DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))),
        s._Code,p._Description, aa._Description, p._Description 

        order by DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'})))

        '''  
query["balance_fact"] = \
    '''--ФАКТ

use IndCons
go
	
	
	DECLARE @Year INT =  2021
Declare @FinalYear int = year(getdate())
DECLARE @YearCnt INT = 1 ;
DECLARE @StartDate DATE = DATEFROMPARTS(@Year, '01','01')
Declare @Finaldate date = DATEFROMPARTS(@FinalYear, '01','01')
DECLARE @EndDate DATE = DATEADD(DAY, -1, DATEADD(YEAR, @YearCnt, @Finaldate));

;WITH
Cal(n) AS
	(
	SELECT 0 UNION ALL SELECT n + 1 FROM Cal
	WHERE n < DATEDIFF(DAY, @StartDate, @EndDate)
	),

FnlDt(d) AS
	(
	SELECT DATEADD(DAY, n, @StartDate) FROM Cal
	where DATEADD(DAY, n, @StartDate)<=DATEADD(MONTH, DATEDIFF(MONTH, -1, GETDATE())-1, -1)
	),
FinalCte AS
	(
	SELECT
	[pk_date] = CONVERT (datetime,d)
	FROM FnlDt
	),
Sectors as 
(select distinct(c._Code) as Sector from dbo._Reference7604 c
 ),--where c._Description not like '%ПЕРЕНЕСТИ%' and  c._Fld10047 =0x01

Sectors_date as
(SELECT
fc.pk_date,
Sector,
1 as 'Тип звіту'
FROM finalCte fc cross join Sectors

--ORDER BY [pk_date]
),

pregroup as(
select 
DATEADD(DAY,CAST(DATEPART(DAY,r._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,r._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,r._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
s._Code as 'Сектор.Код',
CAST(SUM(r._Fld11882) AS NUMERIC(24, 8)) as 'Надходження',1 as 'Тип звіту' 
from dbo._AccumRg11880 r
left join dbo._Reference11879 i on r._Fld11881RRef=i._IDRRef
left join dbo._Reference70 o on o._IDRRef=i._Fld11893RRef
left join dbo._Reference7604 s on s._IDRRef=i._Fld11895RRef

WHERE r._Period >=  '4021-01-01' 

group by DATEADD(DAY,CAST(DATEPART(DAY,r._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,r._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,r._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))),
s._Code
--order by s._Code,
--DATEADD(DAY,CAST(DATEPART(DAY,r._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,r._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,r._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'})))
),

pregroup2 as(
SELECT
DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))) as 'Дата',
s._Code as 'Сектор.Код',
CAST(SUM(f._Fld11547) AS NUMERIC(24, 8)) as 'Витрата',
p._Description as 'Категорія споживача', 1 as 'Тип звіту'    

FROM dbo._AccumRg11545 f
LEFT OUTER JOIN dbo._Reference11544 r --ИзмеренияРегистра_СуточныеРасходыСекторов
ON f._Fld11546RRef = r._IDRRef
LEFT OUTER JOIN dbo._Reference37 c --ДоговорыКонтрагентов
ON r._Fld11563RRef = c._IDRRef
LEFT OUTER JOIN dbo._Reference11759 p --КатегорииПотребителей
ON c._Fld11762RRef = p._IDRRef
left join dbo._Reference7605 aa on c._Fld9487RRef=aa._IDRRef
LEFT OUTER JOIN dbo._Reference70 o --Организации
ON r._Fld11558RRef = o._IDRRef
LEFT OUTER JOIN dbo._Reference7600 t --ТочкиУчета
ON r._Fld11564RRef = t._IDRRef
LEFT OUTER JOIN dbo._Reference7604 s --Секторы
ON r._Fld11899RRef = s._IDRRef


WHERE f._Period >=  '4021-01-01' 

GROUP BY 
DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'}))),
 s._Code,p._Description, aa._Description, p._Description 

--order by DATEADD(DAY,CAST(DATEPART(DAY,f._Period) AS NUMERIC(4)) - 1,DATEADD(MONTH,CAST(DATEPART(MONTH,f._Period) AS NUMERIC(4)) - 1,DATEADD(YEAR,(CAST(DATEPART(YEAR,f._Period) AS NUMERIC(4)) - 2000) - 2000,{ts '2000-01-01 00:00:00'})))
),

pregroup3 as 
(select pregroup2.Дата, pregroup2.[Сектор.Код] , sum(pregroup2.Витрата) as 'Витрата',
sum(iif(pregroup2.[Категорія споживача] = 'Населення',pregroup2.Витрата,null)) as 'Населення',
sum(iif(pregroup2.[Категорія споживача] = 'Промисловість',pregroup2.Витрата,null)) as 'Промисловість', 
sum(iif(pregroup2.[Категорія споживача] = 'Теплоенергетика',pregroup2.Витрата,null)) as 'Теплоенергетика',
sum(iif(pregroup2.[Категорія споживача] = 'Бюджет',pregroup2.Витрата,null)) as 'Бюджет',
sum(iif(pregroup2.[Категорія споживача] = 'Релігія',pregroup2.Витрата,null)) as 'Релігія',
sum(iif(pregroup2.[Категорія споживача] = 'Власні потреби',pregroup2.Витрата,null)) as 'Власні потреби' from pregroup2
group by pregroup2.Дата,pregroup2.[Сектор.Код])


select top (20) Sectors_date.pk_date as "Дата", Sectors_date.Sector as "Сектор.Код",pregroup.Надходження as "Надходження",
pregroup3.Витрата,
pregroup3.Теплоенергетика,
pregroup3.Бюджет,
pregroup3.Релігія,
pregroup3.Населення,
pregroup3.Промисловість,
pregroup3.[Власні потреби],

Sectors_date.[Тип звіту] from pregroup
full join Sectors_date on pregroup.Дата  = Sectors_date.pk_date and pregroup.[Сектор.Код] = Sectors_date.Sector
left outer join pregroup3 on pregroup3.Дата  = Sectors_date.pk_date and pregroup3.[Сектор.Код] =  Sectors_date.Sector
where Sectors_date.pk_date >= '2021-11-01'
order by Sectors_date.Sector , Sectors_date.pk_date
OPTION (MAXRECURSION 0)

'''      
query_coll = query        

		

	
