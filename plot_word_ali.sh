set -e

nj=16
task=test
expdir=./exp/chain_tdnnf/  # exp result directory with special model
ctmdir=./temp/  # path to save the ctm result
datadir=./data/  # data directory include wav.scp & text

. utils/parse_options.sh || exit 1;

expdir=$expdir/decode_$task/
ctmdir=$ctmdir/ctm_$task/
datadir=$datadir/$task/

# get ctm result 
if [ ! -d $ctmdir ]; then
  mkdir -p $ctmdir
fi
lmwt=`cat ${expdir}/scoring_kaldi/best_wer | awk -F"/" '{print $5}' | awk -F"_" '{print $2}'` 
echo "lmwt:" $lmwt
./steps/get_ctm_fast.sh --lmwt $lmwt --frame-shift 0.03 data/$task/ lang/$task/ $expdir $ctmdir
# ctm format : utt_id channel_num start_time phone_dur phone_id

# draw wave form & render phone boundary
ctmfile=$ctmdir/ctm
python3 ./local/plot_word_bowndary.py --ctm $ctmfile --data $datadir --save $ctmdir

