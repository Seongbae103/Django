from dataclasses import dataclass

import googlemaps
import numpy as np
import pandas as pd
from sklearn import preprocessing
import folium
'''
주어진 데이터를 활용해서 서울시내 경찰서 범죄발생과 검거율 현황지도(폴리움)를 작성하시오.
'''
CRIME_MENUS = ["Exit", #0
                "Show Spec",#1
                "Save PolicePosition", #2
                "Save Cctv Population",#3
                "Save Police Normalization",
                "Folium Example",
                "Seoul Folium",#6
                "Create Folium",
                "샘플링",#5
                "모델링",#6
                "학습",#7
                "예측"]#8
crime_meta = {}
crime_menu = {
    "1" : lambda t: t.spec(),
    "2" : lambda t: t.save_police_pos(),
    "3" : lambda t: t.save_cctv_pos(),
    "4" : lambda t: t.save_police_norm(),
    "5" : lambda t: t.folium_example(),
    "6" : lambda t: t.create_folium_data(),
    "7" : lambda t: t.folium_seoul(),
    "8" : lambda t: t.partition(),
    "9" : lambda t: print(),
}
@dataclass
class MyChoroplethVO:
    geo_data = "",
    data = object,
    name = "choropleth",
    columns = [],
    key_on = "feature.id",
    fill_color = "",
    fill_opacity = 0.0,
    line_opacity = 0.0,
    legend_name = "",
    bins = [],
    location = [],
    zoom_start = 0,
    save_path = ''

def MyChoroplethService(vo):
    map = folium.Map(location=vo.location, zoom_start=vo.zoom_start)
    folium.Choropleth(
        geo_data=vo.geo_data,
        data=vo.data,
        name=vo.name,
        columns=vo.columns,
        key_on=vo.key_on,
        fill_color=vo.fill_color,
        fill_opacity=vo.fill_opacity,
        line_opacity=vo.line_opacity,
        legend_name=vo.legend_name,
        bins=vo.bins
    ).add_to(map)
    map.save(vo.save_path)
class Crime:
    def __init__(self):
        self.seoul_crime = pd.read_csv('../../../blog/data/dam_crime/crime_in_seoul.csv')
        cols = ['절도 발생', '절도 검거', '폭력 발생', '폭력 검거']
        self.seoul_crime[cols] = self.seoul_crime[cols].replace(',', '', regex=True).astype(int)  #, regex=True
        self.cctv = pd.read_csv('../../../blog/data/dam_crime/cctv_in_seoul.csv')
        self.pop = pd.read_excel('./fruits-360-5/dam_crime/pop_in_seoul.xls', names = ['자치구','합계','한국인','등록외국인','65세이상고령자'], usecols=[1,3,6,9,13], skiprows=[1,2])
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']
        self.arrest_columns = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']
        self.us_states = pd.read_json('../../../blog/data/dam_crime/us-states.json')
        self.us_unemployment = pd.read_csv('../../../blog/data/dam_crime/us_unemployment.csv')
        self.ko_states = './fruits-360-5/kr-state.json'


    def spec(self):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        [(lambda x: print(f" --- 1.Shape ---\n{x.shape}\n"
                               f"--- 2.Features ---\n{x.columns}\n"
                               f"--- 3.Info ---\n{x.info()}\n"
                               f"--- 4.Case Top1 ---\n{x.head(1)}\n"
                               f"--- 5.Case Bottom1 ---\n{x.tail(3)}\n"
                               f"--- 6.Describe ---{x.describe()}\n"
                               f"--- 7.Describe All ---\n{x.describe(include='all')}"))(i) for i in [self.seoul_crime, self.cctv]]
        print(self.pop)
    def save_police_pos(self): #norminal
        crime = self.seoul_crime
        station_names = []
        for name in crime['관서명']:
            print(f'지역 이름: {name}')
            station_names.append(f'서울{str(name[:-1])}경찰서')
        print(station_names)
        print(f'서울 시내 경찰서는 총 {len(station_names)}개다')
        gmaps = (lambda x: googlemaps.Client(key=x))('')
        print(gmaps.geocode("서울중부경찰서", language='ko'))
        print('API에서 주소추출 시작')
        station_addrs = []
        station_lats = []
        station_lngs = []
        for i, name in enumerate(station_names):
            _ = gmaps.geocode(name, language='ko')
            print(f'name {i} = {_[0].get("formatted_address")}')
            station_addrs.append(_[0].get('formatted_address'))
            _loc = _[0].get('geometry')
            station_lats.append(_loc['location']['lat'])
            station_lngs.append(_loc['location']['lng'])
        gu_names = []
        for name in station_addrs:
            _ = name.split()
            gu_name = [gu for gu in _ if gu[-1]=='구'][0]
            gu_names.append(gu_name)
        crime['구별'] = gu_names
        # 구와 경찰서의 위치가 다른 경우 수작업
        crime.loc[crime['관서명'] == '혜화서', ['구별']] == '종로구'
        crime.loc[crime['관서명'] == '서부서', ['구별']] == '은평구'
        crime.loc[crime['관서명'] == '강서서', ['구별']] == '양천구'
        crime.loc[crime['관서명'] == '종암서', ['구별']] == '성북구'
        crime.loc[crime['관서명'] == '방배서', ['구별']] == '서초구'
        crime.loc[crime['관서명'] == '수서서', ['구별']] == '강남구'
        crime.to_pickle('./save/police_pos.pkl')
        print(pd.read_pickle('./save/police_pos.pkl'))

    def save_cctv_pos(self): #ratio로 판단 -> norminal로 저장
        cctv = self.cctv
        pop = self.pop
        cctv.rename(columns={cctv.columns[0]:'구별'}, inplace=True)
        pop.rename(columns={
            pop.columns[0]:'구별',
            pop.columns[1]:'인구수',
            pop.columns[2]:'한국인',
            pop.columns[3]:'외국인',
            pop.columns[4]:'고령자'
        }, inplace=True)
        print(pop)
        print("*"*100)
        pop.drop(index=26, inplace=True)

        pop['외국인비율'] =pop['외국인'].astype(int)/pop['인구수'].astype(int) *100
        pop['고령자비율'] =pop['고령자'].astype(int)/pop['인구수'].astype(int) *100
        cctv.drop(["2013년도 이전","2014년","2015년","2016년"], axis=1, inplace=True)
        cctv_pop = pd.merge(cctv, pop, on='구별')
        cor1 = np.corrcoef(cctv_pop['고령자비율'], cctv_pop['소계'])
        cor2 = np.corrcoef(cctv_pop['외국인비율'], cctv_pop['소계'])
        print(f'고령자비율과 CCTV의 상관계수 {str(cor1)} \n'
              f'외국인비율과 CCTV의 상관계수 {str(cor2)} ')
        """
         고령자비율과 CCTV 의 상관계수 [[ 1.         -0.28078554]
                                     [-0.28078554  1.        ]] 
         외국인비율과 CCTV 의 상관계수 [[ 1.         -0.13607433]
                                     [-0.13607433  1.        ]]
        r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
        r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
        r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
        r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
        r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
        r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
        r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
        고령자비율 과 CCTV 상관계수 [[ 1.         -0.28078554] 약한 음적 선형관계
                                    [-0.28078554  1.        ]]
        외국인비율 과 CCTV 상관계수 [[ 1.         -0.13607433] 거의 무시될 수 있는
                                    [-0.13607433  1.        ]]                        
         """
        cctv_pop.to_pickle('./save/cctv_pop.pkl')
        print(pd.read_pickle('./save/cctv_pop.pkl'))

    def save_police_norm(self):
        police_pos = pd.read_pickle('./save/police_pos.pkl')
        police = pd.pivot_table(police_pos,index="구별",aggfunc=np.sum)
        police['살인검거율'] = (police['살인 검거'].astype(int) / police['살인 발생'].astype(int)) * 100
        police['강도검거율'] = (police['강도 검거'].astype(int) / police['강도 발생'].astype(int)) * 100
        police['강간검거율'] = (police['강간 검거'].astype(int) / police['강간 발생'].astype(int)) * 100
        police['절도검거율'] = (police['절도 검거'].astype(int) / police['절도 발생'].astype(int)) * 100
        police['폭력검거율'] = (police['폭력 검거'].astype(int) / police['폭력 발생'].astype(int)) * 100
        police.drop(columns={'살인 검거','강도 검거','강간 검거','절도 검거','폭력 검거'}, axis=1, inplace=True)
        for i in self.crime_rate_columns:
            police.loc[police[i] > 100, 1] = 100 # 데이터값의 기간 오류로 100을 넘으면 100으로 계산
        police.rename(columns={
            '살인 발생': '살인',
            '강도 발생': '강도',
            '강간 발생': '강간',
            '절도 발생': '절도',
            '폭력 발생': '폭력'
        }, inplace=True)
        x = police[self.crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler()
        """
        스케일링은 선형변환을 적용하여
        전체 자료의 분포를 평균 0, 분산 1이 되도록 만드는 과정
        """
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        """
        정규화 normalization
        많은 양의 데이터를 처리함에 있어 데이터의 범위(도메인)를 일치시키거나
        분포(스케일)를 유사하게 만드는 작업
        """
        police_norm = pd.DataFrame(x_scaled, columns=self.crime_columns, index=police.index)
        police_norm[self.crime_rate_columns] = police[self.crime_rate_columns]
        police_norm['범죄'] = np.sum(police_norm[self.crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[self.crime_columns], axis=1)
        # police_norm.reset_index(drop=False, inplace=True) # pickle 저장직전 인덱스 해제# fruits-360-5 = tuple(zip(police_norm['구별'], police_norm['범죄']))일 때
        police_norm.reset_index(drop=False, inplace=True) # pickle 저장직전 인덱스 해제
        police_norm.to_pickle('./save/police_norm.pkl')
        print(pd.read_pickle('./save/police_norm.pkl'))

    def folium_example(self):
        us_states = self.us_states
        us_unemployment = self.us_unemployment

        geo_data = "./fruits-360-5/us-states.json"
        state_unemployment = "./fruits-360-5/us_unemployment.csv"
        data = pd.read_csv(state_unemployment)

        bins = list(us_unemployment["Unemployment"].quantile([0, 0.25, 0.5, 0.75, 1]))
        map = folium.Map(location=[48, -102], zoom_start=5)
        folium.Choropleth(
            geo_data=geo_data,
            data=data,
            name="choropleth",
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.5,
            legend_name='Unemployment Rate (%)',
            bins=bins
        ).add_to(map)
        map.save("./save/unemployment2.html")

    '''지도1'''
    def create_folium_data(self):
        data = None
        crime = self.seoul_crime
        police_pos = None
        police_norm = pd.read_pickle('./save/police_norm.pkl')
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1] + '경찰서'))
        station_addrs = []
        station_lats = []
        station_lngs = []
        gmaps = (lambda x: googlemaps.Client(key=x))('')
        for name in station_names:
            t = gmaps.geocode(name, language='ko')
            station_addrs.append(t[0].get('formatted_address'))
            t_loc = t[0].get('geometry')
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])
        police_pos['lat'] = station_lats
        police_pos['lng'] = station_lngs
        temp = police_pos[self.arrest_columns] / police_pos[self.arrest_columns].max()
        police_pos['검거'] = np.sum(temp, axis=1)
        data = tuple(zip(police_norm['구별'], police_norm['범죄']))

        return data
    def folium_seoul(self):
        geo_data = self.ko_states

        data = self.create_folium_data()
        '''지도'''
        map = folium.Map(location=[37.5502, 126.982], zoom_start=12)
        folium.Choropleth(
            geo_data= geo_data,
            data=data,
            name="choropleth",
            columns=["State", "Crime Rate"],
            key_on="feature.id",
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Crime Rate (%)'
        ).add_to(map)
        map.save("./save/crimerate.html")

    def interval(self):
        t = self.cctv
        inter = ['소계','2013년도 이전','2014년','2015년','2016년']
        print(f'--- 구간변수 기초 통계량 --- \n{t[inter].describe()}')

    def partition(self):
        pass

def my_menu(ls):
    for i, j in enumerate(ls):
        print(f"{i}. {j}")
    return input('메뉴선택: ')

if __name__ == '__main__':
    t = Crime()
    while True:
        menu = my_menu(CRIME_MENUS)
        if menu == '0':
            print("종료")
            break
        else:
            try:
                crime_menu[menu](t)
            except KeyError:
                print(" ### Error ### ")