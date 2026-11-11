var delhi = ee.FeatureCollection('FAO/GAUL/2015/level1')
  .filter(ee.Filter.eq('ADM0_NAME', 'India'))
  .filter(ee.Filter.eq('ADM1_NAME', 'Delhi'))
  .geometry();

Map.centerObject(delhi, 10);

function prep(image) {
  var qa = image.select('QA_PIXEL');
  var mask = qa.bitwiseAnd(1 << 0).eq(0)
    .and(qa.bitwiseAnd(1 << 1).eq(0))
    .and(qa.bitwiseAnd(1 << 2).eq(0))
    .and(qa.bitwiseAnd(1 << 3).eq(0))
    .and(qa.bitwiseAnd(1 << 4).eq(0))
    .and(qa.bitwiseAnd(1 << 5).eq(0));
  var sr = image.select(['SR_B4', 'SR_B5']).multiply(0.0000275).add(-0.2);
  var ndvi = sr.normalizedDifference(['SR_B5', 'SR_B4']).rename('ndvi');
  var lst = image.select('ST_B10').multiply(0.00341802).add(149.0)
    .subtract(273.15).rename('lst_c');
  return ndvi.addBands(lst).updateMask(mask);
}

var landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
  .merge(ee.ImageCollection('LANDSAT/LC09/C02/T1_L2'))
  .filterBounds(delhi)
  .filterDate('2023-04-01', '2023-07-01')
  .filter(ee.Filter.lt('CLOUD_COVER', 20))
  .map(prep);

var composite = landsat.median().clip(delhi);
var ndviImage = composite.select('ndvi');
var lst = composite.select('lst_c');

var stats = lst.reduceRegion({
  reducer: ee.Reducer.mean().combine({
    reducer2: ee.Reducer.stdDev(),
    sharedInputs: true
  }),
  geometry: delhi,
  scale: 30,
  maxPixels: 1e9
});

var meanTemp = ee.Number(stats.get('lst_c_mean'));
var stdTemp = ee.Number(stats.get('lst_c_stdDev'));
var hotspotThreshold = meanTemp.add(stdTemp);
var hotspots = lst.gt(hotspotThreshold);

Map.addLayer(lst, {
  min: 20,
  max: 50,
  palette: ['blue', 'cyan', 'green', 'yellow', 'orange', 'red']
}, 'Delhi LST');

Map.addLayer(hotspots.selfMask(), {
  palette: ['red']
}, 'Urban Heat Hotspots');

Map.addLayer(ndviImage, {
  min: -0.2,
  max: 0.8,
  palette: ['blue', 'white', 'yellow', 'green']
}, 'Delhi NDVI');

var uhi = lst.subtract(meanTemp).rename('uhi');

Map.addLayer(uhi, {
  min: -5,
  max: 5,
  palette: ['blue', 'cyan', 'white', 'yellow', 'red']
}, 'Urban Heat Island Map');

var meanNDVI = ndviImage.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: delhi,
  scale: 30,
  maxPixels: 1e9
});

var ndviLstCorrelation = lst.addBands(ndviImage).reduceRegion({
  reducer: ee.Reducer.pearsonsCorrelation(),
  geometry: delhi,
  scale: 30,
  maxPixels: 1e9
});

var uhiNdviCorrelation = uhi.addBands(ndviImage).reduceRegion({
  reducer: ee.Reducer.pearsonsCorrelation(),
  geometry: delhi,
  scale: 30,
  maxPixels: 1e9
});

print('Number of Landsat Images:', landsat.size());
print('Average Delhi Temperature (C):', meanTemp);
print('Temperature Standard Deviation:', stdTemp);
print('Hotspot Threshold (C):', hotspotThreshold);
print('Delhi Mean NDVI:', meanNDVI);
print('NDVI and LST Correlation:', ndviLstCorrelation);
print('UHI and NDVI Correlation:', uhiNdviCorrelation);

Export.image.toDrive({
  image: lst.toFloat(),
  description: 'Delhi_LST_Map',
  fileNamePrefix: 'Delhi_LST_Map',
  region: delhi,
  scale: 30,
  crs: 'EPSG:32643',
  maxPixels: 1e13
});

Export.image.toDrive({
  image: ndviImage.toFloat(),
  description: 'Delhi_NDVI_Map',
  fileNamePrefix: 'Delhi_NDVI_Map',
  region: delhi,
  scale: 30,
  crs: 'EPSG:32643',
  maxPixels: 1e13
});

Export.image.toDrive({
  image: uhi.toFloat(),
  description: 'Delhi_UHI_Map',
  fileNamePrefix: 'Delhi_UHI_Map',
  region: delhi,
  scale: 30,
  crs: 'EPSG:32643',
  maxPixels: 1e13
});