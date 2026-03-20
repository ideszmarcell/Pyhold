# Pyhold Tower Defense - Game Balance Analysis Report

**Analysis Date:** March 20, 2026  
**Game Version:** Current (with reward system implemented)

---

## EXECUTIVE SUMMARY

The game has **moderate balance issues** with three major problems:
1. **Tower cost too high** - requires 13-20 enemy kills to break even
2. **Early game progression is punishing** - limited financial flexibility in waves 1-2
3. **Tower damage lacks variety** - insufficient differentiation between tower types
4. **Tank Enemy severely undervalued** - disproportionately weak reward compared to high HP

---

## 1. ENEMY HP vs TOWER DAMAGE ANALYSIS

### Hits Required to Kill Each Enemy Type

| Enemy Type | Max HP | Arc Tower (12 DMG) | Shock Tower (5 DMG) | Slow Tower (7 DMG) | Notes |
|---|---|---|---|---|---|
| **BasicEnemy** | 24 | 2 hits | 5 hits | 4 hits | Baseline enemy |
| **FastEnemy** | 10 | 1 hit | 2 hits | 2 hits | Dies very quickly |
| **TankEnemy** | 60 | 5 hits | 12 hits | 9 hits | **Too tanky for reward** |
| **ArmoredEnemy** | 18 | 2 hits | 4 hits | 3 hits | Balanced |
| **BossEnemy (Wave 1)** | 360 | 30 hits | 72 hits | 51 hits | Solo tower takes 45-100s |

### Time to Kill (Single Tower)

- **Arc Tower (1500ms cooldown):** kills BasicEnemy in 3sec, Tank in 7.5sec
- **Shock Tower (500ms cooldown):** kills BasicEnemy in 2.5sec, Tank in 6sec
- **Slow Tower (800ms cooldown):** kills BasicEnemy in 3.2sec, Tank in 7.2sec

**Finding:** Shock Tower is actually superior for raw DPS despite lower damage (5 × 2/sec = 10 DPS vs Arc's 8 DPS). This creates an imbalance where Shock Tower should theoretically be more effective than Arc Tower.

---

## 2. TOWER COSTS VS ENEMY REWARDS - Economic Viability

### Cost Recovery Analysis

| Tower Type | Cost | Enemies Needed (Avg Reward) | Enemies from Wave 1 |
|---|---|---|---|
| **Any Tower** | **100 pénz** | **12-20 enemy kills** | **11 total enemies** |

### Detailed Enemy Reward Values

| Enemy Type | HP | Reward Formula | Reward Value | Cost/Reward Ratio |
|---|---|---|---|---|
| BasicEnemy | 24 | HP÷3+2 | **10 pénz** | 10 per kill |
| FastEnemy | 10 | HP÷3+2 | **5 pénz** | 20 kills needed |
| TankEnemy | 60 | HP÷3+2 | **22 pénz** | 4.5 kills needed ✓ |
| ArmoredEnemy | 18 | HP÷3+2 | **8 pénz** | 12.5 kills needed |
| **Boss (Wave 1)** | 360 | formula | **122 pénz** | ✓ Pays for tower |

### Economic Progression - Wave by Wave

#### Wave 1 (11 enemies + Boss)
- Enemies spawn in rotation: Basic, Fast, Tank, Armored, then repeat
- Expected composition: 3× Basic (30¢), 2× Fast (10¢), 2× Tank (44¢), 2× Armored (16¢), 2× Basic (20¢)
- **Wave 1 enemy rewards:** ~120 pénz
- **Boss reward:** +122 pénz  
- **Boss pre-spawn bonus:** +100 pénz
- **Total Wave 1 income:** ~342 pénz
- **Starting capital:** 200 pénz
- **After Wave 1:** ~542 pénz ✓

#### Wave 2 (14 enemies + Boss)
- More enemies = proportionally more money
- **Expected wave income:** ~165 pénz
- **Boss reward:** +152 pénz (122 + 10×3)
- **Boss bonus:** +100 pénz
- **Total Wave 2 income:** ~417 pénz
- **Can sustain 4-5 towers** ✓

**Finding:** **Economic viability becomes solid from Wave 2 onwards**, but Wave 1 is extremely tight. Players must either:
1. Win Wave 1 with only starting 2 towers
2. Or use no upgrades and save money for Wave 2

---

## 3. TOWER UPGRADE COSTS - Reasonability Check

### Upgrade Cost Formula: `25 × level`

| From → To | Cost | Cumulative | Description |
|---|---|---|---|
| Level 1→2 | 25 pénz | 25 pénz | +20% damage, +15% range, +100ms faster |
| Level 2→3 | 50 pénz | 75 pénz | +20% damage, +15% range, +100ms faster |
| Level 3→4 | 75 pénz | 150 pénz | +20% damage, +15% range, +100ms faster |
| Level 4→5 | 100 pénz | 250 pénz | **Full tower cost worth of upgrades** |

### Cost-Benefit Analysis

**Per Level Upgrade Gains:**
- Damage: +20% (Arc 12→14.4 HP/12→10.8 DPS improvement)
- Range: +15% (Arc 3.0→3.45 tiles)
- Attack speed: -10% cooldown (Arc 1500ms→1350ms)

**Breakeven Analysis:**
- At Level 1→2: 25 pénz for +20% damage = **need to kill 2-3 enemies to justify** ✓ Fast payoff
- At Level 4→5: 100 pénz for +20% damage = **need to kill 10+ enemies to justify** ⚠️ Questionable late-game investment
- **Scaling issue:** Late-game upgrades become inefficient compared to buying new towers

**Finding:** **Upgrade progression is well-balanced early game but becomes inefficient at Level 4-5**. Players should prefer building new towers over upgrading to max level.

---

## 4. TOWER DAMAGE OUTPUT VS ENEMY HP - Kill Efficiency Matrix

### Time to Kill (With Attack Cooldowns)

```
SHOCK TOWER (Best DPS = 5 DMG/500ms)
- BasicEnemy (24 HP):  1000ms (2 hits)
- FastEnemy (10 HP):    500ms (1 hit)
- TankEnemy (60 HP):   6000ms (12 hits) ⚠️ SLOW
- ArmoredEnemy (18 HP): 1000ms (2 hits)

ARC TOWER (Most Reliable = 12 DMG/1500ms)
- BasicEnemy (24 HP):  1500ms (2 hits)
- FastEnemy (10 HP):   1500ms (1 hit)
- TankEnemy (60 HP):   7500ms (5 hits) ✓ Better than Shock
- ArmoredEnemy (18 HP): 1500ms (2 hits)

SLOW TOWER (Utility = 7 DMG/800ms)
- BasicEnemy (24 HP):  1600ms (2 hits)
- FastEnemy (10 HP):   1600ms (2 hits) ⚠️ Slower than Shock
- TankEnemy (60 HP):   7200ms (9 hits)
- ArmoredEnemy (18 HP): 1600ms (2 hits)
```

### Tower Effectiveness Rankings by Enemy

| Enemy | Best | Second | Worst | Winner Margin |
|---|---|---|---|---|
| **BasicEnemy** | Arc/Shock (1000-1500ms) | Slow (1600ms) | None | Marginal |
| **FastEnemy** | Shock (500ms) | Arc/Slow (1500-1600ms) | Slow | Arc is 3x slower |
| **TankEnemy** | Arc (7500ms) | Slow (7200ms) | Shock (6000ms) | Shock actually best! |
| **ArmoredEnemy** | Arc/Shock (1000-1500ms) | Slow (1600ms) | None | All similar |

**Critical Finding:** **SHOCK TOWER is strictly superior to ARC TOWER** due to DPS advantage. Arc Tower should be 15-20 damage, not 12!

---

## 5. OVERALL PROGRESSION - Wave 1 to Wave N Balance

### Money Flow by Wave

| Wave | Wave 1 | Wave 2 | Wave 3 | Wave 5 |
|---|---|---|---|---|
| Enemies | 11 | 14 | 17 | 23 |
| Expected Income | 120¢ | 165¢ | 210¢ | 310¢ |
| Boss Reward | +122¢ | +152¢ | +182¢ | +222¢ |
| Bonus Pre-Boss | +100¢ | +100¢ | +100¢ | +100¢ |
| **Total Wave Income** | **342¢** | **417¢** | **492¢** | **632¢** |

### Player Resources Timeline

```
Start:              200 pénz
After Wave 1:       542 pénz (2 towers + 342 income)
After Wave 2:       959 pénz (4-5 towers possible)
After Wave 3:     1451 pénz (ability to fully upgrade towers)
After Wave 5:     3083 pénz (6+ fully upgraded towers)
```

### Progression Assessment

✅ **Wave 1-2:** Tight but manageable with good play  
✅ **Wave 3+:** Comfortable, player has resource options  
⚠️ **Issue:** Wave 1 requires perfect play - no room for tower loss or building mistakes

---

## MAJOR BALANCE ISSUES IDENTIFIED

### 🔴 CRITICAL ISSUE #1: Tank Enemy Severely Undervalued

- **HP:** 60 (2.5× more than BasicEnemy's 24)
- **Reward:** 22 pénz (2.2× more than BasicEnemy's 10)
- **Problem:** Reward scaling doesn't match HP complexity
- **Example:** TankEnemy takes 30 hits from Shock Tower vs BasicEnemy's 5 hits
- **Recommendation:** Increase TankEnemy reward from 22 → 30 pénz

### 🔴 CRITICAL ISSUE #2: Tower Cost Too High (Wave 1)

- **Cost per tower:** 100 pénz
- **Wave 1 income:** 342 pénz
- **Result:** Players can only buy 3 towers total in Wave 1 (200 start + 342 income = 542)
- **Problem:** No money for ANY upgrades if towers are destroyed
- **Recommendation:** Either reduce to 75 pénz OR increase Wave 1 enemy count to 13

### 🟡 MAJOR ISSUE #3: Arc Tower Underpowered vs Shock Tower

- **Arc Tower:** 12 damage, 1500ms cooldown = 8 DPS
- **Shock Tower:** 5 damage, 500ms cooldown = 10 DPS
- **Problem:** No reason to ever build Arc Tower vs Shock Tower
- **Recommendation:** Increase Arc Tower damage to 15-16 (making it 10-10.7 DPS), justifying longer cooldown for higher single-hit damage

### 🟡 MAJOR ISSUE #4: Slow Tower Has Purpose Crisis

- **Damage:** 7 (between Shock's 5 and Arc's 12)
- **Cooldown:** 800ms (between them)
- **DPS:** 8.75 (better than Arc but worse than Shock)
- **Effect:** Slows enemies by 40% for 2 seconds
- **Problem:** Utility doesn't justify middle-ground damage/cooldown
- **Recommendation:** Either increase damage to 9+ OR increase slow effect to 50%+ to make it worthwhile as alternatives

### 🟡 MAJOR ISSUE #5: Early Game Extremely Fragile

- **Risk:** If even 1 tower dies before Wave 2, player is in critical resource shortage
- **Boss damage:** 25 + wave×5 = 25 damage per hit at Wave 1
- **Tower HP:** 150
- **Risk window:** Boss can destroy towers in 6 hits (~7-8 seconds combat time)
- **Recommendation:** Either increase tower HP to 200 or reduce boss damage to 20

---

## SPECIFIC NUMERICAL RECOMMENDATIONS

### 1. Enemy Reward Adjustments

```python
# Current System (HP // 3 + 2)
BasicEnemy: 24 HP → 10 pénz ✓ OK
FastEnemy: 10 HP → 5 pénz   ✓ OK
TankEnemy: 60 HP → 22 pénz  ✗ LOW - Change to 28 pénz
ArmoredEnemy: 18 HP → 8 pénz ✓ OK
Boss: 360 + wave×30 → 122 + wave×10 ✓ OK
```

### 2. Tower Damage Rebalancing

```python
# Current Damage Values
ArcTower:    12 damage → INCREASE to 16 damage (justifies long cooldown)
ShockTower:  5 damage  → KEEP (balanced as rapid-fire option)
SlowTower:   7 damage  → INCREASE to 10 damage (make it viable middle option)
```

### 3. Tower Cost Options (Choose ONE)

**Option A (Recommended):** Reduce tower cost
```python
AR_TORONY = 100  → Change to 75 pénz
# Allows players to buy 4 towers Wave 1 (200 + 342 = 542 = 5.4 towers)
```

**Option B:** Keep at 100, increase Wave 1 enemy count
```python
# Wave formula: 8 + (wave * 3)
# Change to: 10 + (wave * 3)
# Wave 1: 13 enemies (not 11) = ~147 pénz income
# Total: 200 + 447 = 647 pénz (6 towers possible)
```

### 4. Tower HP Suggestion

```python
# Current: max_hp = 150
# Change to: max_hp = 180-200
# Gives towers more durability against early boss damage
```

---

## ECONOMIC BALANCE SUMMARY TABLE

| Metric | Current | Verdict | Recommendation |
|---|---|---|---|---|
| Tower Cost | 100 pénz | ⚠️ Too High | Reduce to 75 or adjust wave count |
| Upgrade L1→2 | 25 pénz | ✓ Good | Keep (excellent early game value) |
| Upgrade L4→5 | 100 pénz | ⚠️ Poor | Consider reducing to 75 |
| Tank Enemy HP | 60 | ⚠️ High Skew | Adjust reward to 28 |
| Boss HP Wave 1 | 360 | ✓ Good | Scales appropriately |
| Tower DPS Gap | Arc 8 vs Shock 10 | ⚠️ Major Gap | Increase Arc to 16 damage |
| Progression Tightness | Wave 1 | 🔴 Risky | Add safety margin |

---

## CONCLUSION

The game has **solid economic structure from Wave 2 onwards**, but suffers from:

1. **Wave 1 is unforgiving** - requires nearly perfect play with no losses
2. **Tower balance is skewed** - Shock Tower is strictly better than Arc/Slow Tower
3. **Tank Enemy undervalued** - should grant more reward for its HP investment
4. **No financial safety net** - losing one tower cascades into economic failure

**Implement at minimum:** 
- Tank Enemy reward: 22 → 28 pénz
- Arc Tower damage: 12 → 16
- Tower cost: 100 → 75 pénz

**Implement ideally:**
- All three above + Tower HP 150 → 180 + Slow Tower damage 7 → 10

These changes will create a more forgiving progression curve and encourage strategic tower variety.

