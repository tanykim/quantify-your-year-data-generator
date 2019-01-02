import json
import _setup

# settings
settings = dict(
    twitter=dict(
        gender=_setup.GENDER,
        pastVerb='tweeted',
        type='count',
        metric='tweet',
        dataSource=dict(name='Twitter', url='http://www.twitter.com/'),
        considerFrequency=False
    ),
    location=dict(
        gender=_setup.GENDER,
        # change home if necessary
        pastVerb='stayed at home',
        type='duration',
        metric='hour',
        dataSource=dict(name='Google Maps', url='https://www.google.com/maps/timeline'),
        considerFrequency=False,
        decimal=1
    ),
    steps=dict(
        gender=_setup.GENDER,
        pastVerb='walked',
        type='count',
        metric='step',
        dataSource=dict(name='Apple iOS Health', url='https://www.apple.com/ios/health/'),
        considerFrequency=False
    ),
    floors=dict(
        gender=_setup.GENDER,
        pastVerb='climbed',
        type='count',
        metric='floor',
        dataSource=dict(name='Apple iOS Health', url='https://www.apple.com/ios/health/'),
        considerFrequency=False
    ),
    electricity=dict(
        # my house is female
        gender='female',
        pastVerb='used electricity',
        type='usage',
        metric='kWh',
        dataSource=dict(name='PG&E', url='https://www.pge.com/'),
        decimal=2,
        hasNegative=True,
        isReverse=True,
        considerFrequency=False
    ),
    driving=dict(
        # my car is male
        gender='male',
        pastVerb='drove',
        type='distance',
        metric='mile',
        dataSource=dict(name='Metromile', url='https://www.metromile.com/'),
        decimal=2,
        considerFrequency=True
    )
)

# save setting as json
def save_setting(name, dataset_name, data_type):
    fd = open(_setup.FOLDER + 'settings/' + name + '-' + dataset_name + '-' + str(_setup.YEAR) + '.json', 'w', encoding='utf8')
    setting = dict(
        year=_setup.YEAR,
        author=name,
        topic=' '.join(dataset_name.split('-')),
    )
    json_data = json.dumps({**setting, **settings[data_type]}, separators=(',',':'), indent=2, ensure_ascii=False)
    fd.write(json_data)
    fd.close()

# save data as json
def save_dataset(dataset, name, dataset_name, data_type):
    fd = open(_setup.FOLDER + 'data/' + name + '-' + dataset_name + '-' + str(_setup.YEAR) + '.json', 'w', encoding='utf8')
    json_data = json.dumps(dataset, separators=(',',':'), indent=2, ensure_ascii=False)
    fd.write(json_data)
    fd.close()

    # save setting files as well
    save_setting(name, dataset_name, data_type)
