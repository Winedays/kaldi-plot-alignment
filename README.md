# kaldi-plot-alignment
This project generate the ctm file of a decode result and plot the alignment graph of each utterance using Kaldi.

## Getting started
copy `plot_word_ali.sh` and `plot_word_bowndary.py` to a kaldi project local directory.
```
cp plot_word_ali.sh plot_word_bowndary.py $Kaldi_root/egs/$project/local/
```

Run the script `plot_word_ali.sh` in project directory .  
It assume the decode directory was naming with $exp_dir/decode_$task 
```
cd $Kaldi_root/egs/$project 
./local/plot_word_ali.sh --task $task --exp_dir $exp_dir --ctmdir $ctmdir --savedir $savedir
```
- task: test set directory name in data dir.
- exp_dir: exp result directory with special model
- ctmdir: path to save the ctm result
- savedir: path to save the wave alignment graph

## Graph sample
![example](https://i.imgur.com/yzMUTns.png)
