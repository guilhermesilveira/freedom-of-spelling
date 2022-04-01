include "globals.mzn";

%% Parameters

% parameter space for all 3 cuts
array[int] of int: SPACE_1;
array[int] of int: SPACE_2;
array[int] of int: SPACE_3;

% clubs, hearts, spades, diamonds, ace to king
enum CARD = { C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,
              H1,H2,H3,H4,H5,H6,H7,H8,H9,H10,H11,H12,H13,
              S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12,S13,
              D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,D11,D12,D13 };


% length of all card names
array[CARD] of int: LENGTHS;

%% Variables

array[CARD] of var int: position;

% a range function
function array[int] of int:
  cut(int: from, int: length) =
    from + 1..from + length;

% number of cards in each packet    
function array[1..4] of int:
  lengths(array[1..5] of int: cuts,
          array[1..4] of int: seqs) =
    [cuts[seqs[i] + 1] - cuts[seqs[i]] | i in 1..4];

% simulate the deck procedure
function array[1..52] of int:
  simulate(array[1..5] of int: cuts,
           array[1..4] of int: seqs) =
  let {
   array[1..4] of int: len = lengths(cuts, seqs),
%    array[1..4] of int: spreads = [sum([len[j] | j in 1..4 where j <= i]) | i in 1..4],
   } in cut(cuts[seqs[1]], len[1]) ++ 
        cut(cuts[seqs[2]], len[2]) ++ 
        cut(cuts[seqs[3]], len[3]) ++ 
        cut(cuts[seqs[4]], len[4]);


% all cards should be between 1 and 52
constraint forall(c in CARD)(position[c] >= 1 /\
                             position[c] <= 52);

% all cards should be at distinct positions
constraint all_different(position);

% at least one should be in its position
predicate in_its_position(array[1..5] of int: cuts,
                          array[1..4] of int: seqs) =
  let{array[int] of int: deck = simulate(cuts, seqs)}
    in exists(c in CARD)
             (position[c]==deck[LENGTHS[c]] \/
             position[c]==deck[LENGTHS[c] + 1]);

% for all possible values there should be one solution
constraint
  forall(cut_1 in SPACE_1,
         cut_2 in SPACE_2,
         cut_3 in SPACE_3,
         seq_1 in 1..4,
         seq_2 in 1..4 diff {seq_1},
         seq_3 in 1..4 diff {seq_1, seq_2},
         seq_4 in 1..4 diff {seq_1, seq_2, seq_3}
         where cut_2 > cut_1 /\ cut_3 > cut_2) (
         in_its_position([0, cut_1, cut_2, cut_3, 52],
                         [seq_1, seq_2, seq_3, seq_4])
                         );

solve satisfy;

output ["SPACE_1 = ", show(SPACE_1), "\n"];
output ["SPACE_2 = ", show(SPACE_2), "\n"];
output ["SPACE_3 = ", show(SPACE_3), "\n"];
output ["position = ", show(position), "\n"];
output ["cards = ", show([CARD[i] | i in position])];
