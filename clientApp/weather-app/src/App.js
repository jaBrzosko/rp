import React, { useState, useEffect, useRef } from 'react';
import DatePicker from 'react-datepicker';
import axios from 'axios';
import './App.css';
import "react-datepicker/dist/react-datepicker.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faStop, faRedo, faCaretLeft, faCaretRight } from '@fortawesome/free-solid-svg-icons';


function App() {

  const initialColors = Array(121).fill({
    bottomLeftColor: 'rgba(0, 0, 0, 0)',
    bottomRightColor: 'rgba(0, 0, 0, 0)',
    topLeftColor: 'rgba(0, 0, 0, 0)',
    topRightColor: 'rgba(0, 0, 0, 0)'
  });
  
  const [data, setData] = useState([]);
  const [date, setDate] = useState(null);
  const [currentMonth, setCurrentMonth] = useState(null)
  const [maxDaysInCurrentMonth, setMaxDaysInCurrentMonth] = useState(0)
  const [currentDay, setCurrentDay] = useState(0);
  const [currentHour, setCurrentHour] = useState(0);
  const [dataReady, setDataReady] = useState(false)
  const [isAnimationPlaying, setIsAnimationPlaying] = useState(false)
  const intervalRef = useRef(null);
  const currentIterationRef = useRef(0)

  // temperatures
  const [northWestTemperature, setNorthWestTemperature] = useState(null)
  const [southWestTemperature, setSouthWestTemperature] = useState(null)
  const [northEastTemperature, setNorthEastTemperature] = useState(null)
  const [southEastTemperature, setSouthEastTemperature] = useState(null)
  const [centerTemperature, setCenterTemperature] = useState(null)

  useEffect(() => {

    const calculateColors = () => {
      const calculatedColors = []
      for (let i = 0; i < 12; ++i) {
        calculatedColors.push([])
      }
      var dataIndex = 0;
      const defaultColor = "rgba(0, 0, 0, 1)"
      for (let i = 0; i < 12; ++i) {
        for (let j = 0; j < 12; ++j) {
          if (i === 0 || i === 11 || j === 0 || j === 11) {
            calculatedColors[i].push(defaultColor)
          }
          else {
            const temperatureString = data.points[dataIndex].date_temperature[currentIterationRef.current].temperature;
            var calculatedColor = getColorForTemperature(parseFloat(temperatureString))
            calculatedColors[i].push(calculatedColor)
            if (dataIndex === 25) {
              setNorthWestTemperature(temperatureString)
            }
            else if (dataIndex === 41) {
              setNorthEastTemperature(temperatureString)
            }
            else if (dataIndex === 57) {
              setSouthWestTemperature(temperatureString)
            }
            else if (dataIndex === 61) {
              setCenterTemperature(temperatureString)
            }
            else if (dataIndex === 95) {
              setSouthEastTemperature(temperatureString)
            }
            dataIndex++;
          }
        }
      }
      var colors = []
      for (let i = 0; i < 11; ++i) {
        for (let j = 0; j < 11; ++j) {
          colors.push({
            bottomLeftColor: calculatedColors[i][j + 1],
            bottomRightColor: calculatedColors[i + 1][j + 1],
            topLeftColor: calculatedColors[i][j],
            topRightColor: calculatedColors[i + 1][j]
          });
        }
      }
      return colors;
    }

    const interpolateColor = (color1, color2, factor) => {
      const result = color1.slice();
      for (let i = 0; i < 3; i++) {
        result[i] = Math.round(result[i] + factor * (color2[i] - color1[i]));
      }
      return result;
    };

    const getColorForTemperature = (temperature) => {
      const colors = [
        { temperature: -25, color: [0, 0, 255] },    // Deep blue
        { temperature: -16, color: [128, 128, 255] },    // Blue
        { temperature: -8, color: [1, 255, 255] },    // Light blue
        { temperature: 0, color: [255, 255, 255] },  // White
        { temperature: 8, color: [255, 242, 178] },     // Yellow
        { temperature: 16, color: [255, 103, 0] },     // Orange
        { temperature: 25, color: [255, 0, 0] }      // Red
      ];

      if (temperature <= -20) return 'rgb(0, 0, 255, 0.5)';
      if (temperature >= 20) return 'rgb(255, 0, 0, 0.5)';

      let lower, upper;
      for (let i = 0; i < colors.length - 1; i++) {
        if (temperature >= colors[i].temperature && temperature <= colors[i + 1].temperature) {
          lower = colors[i];
          upper = colors[i + 1];
          break;
        }
      }

      const range = upper.temperature - lower.temperature;
      const factor = (temperature - lower.temperature) / range;

      const color = interpolateColor(lower.color, upper.color, factor);

      return `rgb(${color[0]}, ${color[1]}, ${color[2]}, 0.5)`;
    };

    if (isAnimationPlaying) {
      intervalRef.current = setInterval(() => {
        var end = false;

        if (currentDay === maxDaysInCurrentMonth && currentHour === 23) {
          end = true;
        }

        if (end) {
          setIsAnimationPlaying(false);
          clearInterval(intervalRef.current);
          setCurrentDay(0)
          setCurrentHour(0)
          currentIterationRef.current = 0;
        }
        else {
          var colors = calculateColors()
          colors.forEach((element, i) => {
            const index = i + 1;
            document.documentElement.style.setProperty(`--bottom-left-color-${index}`, element.topRightColor);
            document.documentElement.style.setProperty(`--top-right-color-${index}`, element.bottomLeftColor);
            document.documentElement.style.setProperty(`--bottom-right-color-${index}`, element.bottomRightColor);
            document.documentElement.style.setProperty(`--top-left-color-${index}`, element.topLeftColor);
          });

          setCurrentHour((prevHour) => {
            return prevHour !== 23 ? prevHour + 1 : 0;
          });
  
          setCurrentDay((prevDay) => {
            return currentHour === 23 ? prevDay + 1 : prevDay;
          });

          currentIterationRef.current += 1
        }
      }, 100);
    }

    return () => clearInterval(intervalRef.current);
  }, [isAnimationPlaying, currentDay, currentHour, data.points, maxDaysInCurrentMonth]);


  const stopAnimation = () => {
    setIsAnimationPlaying(false);
    clearInterval(intervalRef.current);
  };


  const endAnimation = () => {
    setIsAnimationPlaying(false);
    clearInterval(intervalRef.current);
    setCurrentDay(0)
    setCurrentHour(0)
    currentIterationRef.current = 0
  };

  const fetchData = async (year, month) => {
    try {
      const response = await axios.get(`http://localhost:5000/temperature/${year}/${month}`);
      setData(response.data);
      console.log("Successfully loaded.")
      console.log(response.data.points)
      setDataReady(true)
    } catch (error) {
      console.log("Error: " + error)
      setDataReady(false)
    }
  };

  const handleDatePickerChange = (newValue) => {
    setDate(newValue)
    const month = newValue.getMonth() + 1;
    setCurrentMonth(month)
    const year = newValue.getFullYear();
    const maxDays = new Date(year, month, 0).getDate();
    setMaxDaysInCurrentMonth(maxDays)
    setCurrentDay(1)
    setDataReady(false)
    fetchData(year, month)
  }

  const calculateColors = () => {
    const calculatedColors = []
    for (let i = 0; i < 12; ++i) {
      calculatedColors.push([])
    }
    var dataIndex = 0;
    const defaultColor = "rgba(0, 0, 0, 1)"
    for (let i = 0; i < 12; ++i) {
      for (let j = 0; j < 12; ++j) {
        if (i === 0 || i === 11 || j === 0 || j === 11) {
          calculatedColors[i].push(defaultColor)
        }
        else {
          const temperatureString = data.points[dataIndex].date_temperature[currentIterationRef.current].temperature;
          var calculatedColor = getColorForTemperature(parseFloat(temperatureString))
          calculatedColors[i].push(calculatedColor)
          if (dataIndex === 25) {
            setNorthWestTemperature(temperatureString)
          }
          else if (dataIndex === 41) {
            setNorthEastTemperature(temperatureString)
          }
          else if (dataIndex === 57) {
            setSouthWestTemperature(temperatureString)
          }
          else if (dataIndex === 61) {
            setCenterTemperature(temperatureString)
          }
          else if (dataIndex === 95) {
            setSouthEastTemperature(temperatureString)
          }
          dataIndex++;
        }
      }
    }
    var colors = []
    for (let i = 0; i < 11; ++i) {
      for (let j = 0; j < 11; ++j) {
        colors.push({
          bottomLeftColor: calculatedColors[i][j + 1],
          bottomRightColor: calculatedColors[i + 1][j + 1],
          topLeftColor: calculatedColors[i][j],
          topRightColor: calculatedColors[i + 1][j]
        });
      }
    }
    return colors;
  }

  const interpolateColor = (color1, color2, factor) => {
    const result = color1.slice();
    for (let i = 0; i < 3; i++) {
      result[i] = Math.round(result[i] + factor * (color2[i] - color1[i]));
    }
    return result;
  };

  const getColorForTemperature = (temperature) => {
    const colors = [
      { temperature: -25, color: [0, 0, 255] },    // Deep blue
      { temperature: -16, color: [128, 128, 255] },    // Blue
      { temperature: -8, color: [1, 255, 255] },    // Light blue
      { temperature: 0, color: [255, 255, 255] },  // White
      { temperature: 8, color: [255, 242, 178] },     // Yellow
      { temperature: 16, color: [255, 103, 0] },     // Orange
      { temperature: 25, color: [255, 0, 0] }      // Red
    ];

    if (temperature <= -20) return 'rgb(0, 0, 255, 0.5)';
    if (temperature >= 20) return 'rgb(255, 0, 0, 0.5)';

    let lower, upper;
    for (let i = 0; i < colors.length - 1; i++) {
      if (temperature >= colors[i].temperature && temperature <= colors[i + 1].temperature) {
        lower = colors[i];
        upper = colors[i + 1];
        break;
      }
    }

    const range = upper.temperature - lower.temperature;
    const factor = (temperature - lower.temperature) / range;

    const color = interpolateColor(lower.color, upper.color, factor);

    return `rgb(${color[0]}, ${color[1]}, ${color[2]}, 0.5)`;
  };

  const handleLeftArrowClick = () => {
    if (maxDaysInCurrentMonth === 0 || !dataReady) return;
    if (currentDay === 0 && currentHour === 0) return;
    var colors = calculateColors()
    colors.forEach((element, i) => {
      const index = i + 1;
      document.documentElement.style.setProperty(`--bottom-left-color-${index}`, element.topRightColor);
      document.documentElement.style.setProperty(`--top-right-color-${index}`, element.bottomLeftColor);
      document.documentElement.style.setProperty(`--bottom-right-color-${index}`, element.bottomRightColor);
      document.documentElement.style.setProperty(`--top-left-color-${index}`, element.topLeftColor);
    });

    setCurrentHour((prevHour) => {
      return prevHour !== 0 ? prevHour - 1 : 23;
    });

    setCurrentDay((prevDay) => {
      return currentHour === 0 ? prevDay - 1 : prevDay;
    });

    currentIterationRef.current -= 1
  }

  const handleRightArrowClick = () => {
    if (maxDaysInCurrentMonth === 0 || !dataReady) return;
    if (currentDay === maxDaysInCurrentMonth && currentHour === 23) return;
    var colors = calculateColors()
    colors.forEach((element, i) => {
      const index = i + 1;
      document.documentElement.style.setProperty(`--bottom-left-color-${index}`, element.topRightColor);
      document.documentElement.style.setProperty(`--top-right-color-${index}`, element.bottomLeftColor);
      document.documentElement.style.setProperty(`--bottom-right-color-${index}`, element.bottomRightColor);
      document.documentElement.style.setProperty(`--top-left-color-${index}`, element.topLeftColor);
    });

    setCurrentHour((prevHour) => {
      return prevHour !== 23 ? prevHour + 1 : 0;
    });

    setCurrentDay((prevDay) => {
      return currentHour === 23 ? prevDay + 1 : prevDay;
    });

    currentIterationRef.current += 1
  }

  const handleStartToggleButton = () => {
    if (isAnimationPlaying || data === null || !dataReady) return;
    setIsAnimationPlaying(true)
  }

  const handleStopToggleButton = () => {
    stopAnimation()
  }

  const handleRestartToggleButton = () => {
     endAnimation()
     setCurrentDay(1)
     setIsAnimationPlaying(true)
  }

  const getDayString = () => {
    if (currentDay === 0 || currentMonth === 0) return "";
    var result = ` of ${currentDay}`
    if (currentDay > 3) result += "th"
    else if (currentDay === 1) result += "st"
    else if (currentDay === 2) result += "nd"
    else result += "rd"
    const date = new Date(2023, currentMonth - 1);
    result += ` ${date.toLocaleString('en-US', { month: 'long' })}`;
    return result;
  }

  return (
    <div className="App">
      <div className="container">
        <div className="spacer-menu"/>
        <div className="menu">
          <div className="title">
            Temperature Visualizer in Poland
          </div>
          <div className="legend-container">
            <div className="legend"/>
            <div className="legend-text-container">
              <div className="legend-text legend-text-botom">-25&deg;C</div>
              <div className="legend-text">-12&deg;C</div>
              <div className="legend-text">0&deg;C</div>
              <div className="legend-text">12&deg;C</div>
              <div className="legend-text legend-text-top">25&deg;C</div>
            </div>
          </div>
          <div className='datepicker-container'>
            <DatePicker
              selected={date}
              onChange={date => handleDatePickerChange(date)}
              dateFormat="MMMM yyyy"
              showMonthYearPicker
              showFullMonthYearPicker
              placeholderText="Select Month and Year"
              className="custom-datepicker"
            />
          </div>
          <div className="current-day-container">
            <div className="current-day-subcontainer">
              <div>
                <FontAwesomeIcon icon={faCaretLeft} size="5x" className="arrow" onClick={handleLeftArrowClick}/>
              </div>
              <div className="current-day">
                {currentHour === -1 ? "00:00" : currentHour < 10 ? `0${currentHour}:00` : `${currentHour}:00`}
              </div>
              <div>
                <FontAwesomeIcon icon={faCaretRight} size="5x" className="arrow" onClick={handleRightArrowClick}/>
              </div>
            </div>
            <div className="current-day-title">
              Current hour {getDayString()}
            </div>
          </div>
          <div>
          <div className="toggle-button">
              <div className="toggle start-toggle" onClick={() => handleStartToggleButton()}>
                <FontAwesomeIcon icon={faPlay} />
              </div>
              <div className="toggle stop-toggle" onClick={() => handleStopToggleButton()}>
                <FontAwesomeIcon icon={faStop} />
              </div>
              <div className="toggle restart-toggle" onClick={() => handleRestartToggleButton()}>
                <FontAwesomeIcon icon={faRedo} />
              </div>
            </div>
          </div>
        </div>
        <div className="spacer-menu"/>
        <div className="image">
          <img src="./Poland.png" alt="Poland" />
          <div className="overlay-grid">
            {initialColors.map((color, index) => (
              <div
                key={index}
                className={`overlay-panel overlay-panel-${index}`}
              >
                {index === 25 && northWestTemperature !== null ? `${Math.floor(parseFloat(northWestTemperature))}\u00B0C` : null}
                {index === 41 && northEastTemperature !== null ? `${Math.floor(parseFloat(northEastTemperature))}\u00B0C` : null}
                {index === 57 && southWestTemperature !== null ? `${Math.floor(parseFloat(southWestTemperature))}\u00B0C` : null}
                {index === 61 && centerTemperature !== null ? `${Math.floor(parseFloat(centerTemperature))}\u00B0C` : null}
                {index === 95 && southEastTemperature !== null ? `${Math.floor(parseFloat(southEastTemperature))}\u00B0C` : null}
              </div>
            ))}
          </div>
        </div>
        <div className="spacer-right"/>
      </div>
    </div>
  );
}

export default App;
