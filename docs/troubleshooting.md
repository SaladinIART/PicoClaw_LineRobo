# Troubleshooting Guide

## Robot Issues

### Robot Won't Follow the Line

**Problem**: Robot moves randomly or stays stationary.

**Diagnosis**:
1. Check if line sensor detects the line (should read different values on black vs. white)
2. Verify motors spin when connected to power
3. Test motor driver connections

**Solutions**:
- **Sensor not detecting**: Clean sensor lens, adjust sensitivity threshold
- **Motors not spinning**: Check motor connections, verify PWM signals
- **Steering too aggressive**: Reduce steering gain parameter
- **Steering too weak**: Increase steering gain parameter

### Robot Loses Line Frequently

**Problem**: Robot leaves the line often.

**Causes**:
- Line is too faint or track too narrow
- Sensor positioned incorrectly
- Steering gain miscalibrated
- Track too curved for current settings

**Solutions**:
1. Ensure high contrast between line and floor (use black tape on white surface)
2. Center sensor over line
3. Fine-tune steering gain:
   - Too high (> 2.0): Oscillates side-to-side
   - Too low (< 0.5): Doesn't correct enough
4. Slow down motor speed on curves

### Robot Stuck in Recovery Loop

**Problem**: Robot continuously tries to recover without success.

**Diagnosis**:
1. Line is truly missing from track
2. Recovery timeout too long
3. Search pattern ineffective

**Solutions**:
- Add the missing line to track
- Reduce recovery timeout (give up faster)
- Adjust search rotation speed
- Check battery voltage (may affect motor performance)

## Communication Issues

### Robot Not Connecting to WiFi

**Problem**: Telemetry not being received.

**Check**:
1. WiFi credentials in firmware are correct
2. Router is accessible from robot location
3. MQTT broker is running

**Solutions**:
```bash
# Verify WiFi on robot
# (Connect via USB and check REPL for connection status)

# Check broker is running
docker-compose ps mosquitto
# Should show "Up"

# Test MQTT connectivity
docker-compose exec mosquitto mosquitto_sub -t 'robot/#'