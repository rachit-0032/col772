import json
import argparse


def read_cli():
    parser = argparse.ArgumentParser(description="Evaluation Script.")

    parser.add_argument(
        "-sol_path", "--solution_path",
        help="Output file to be scored",
        required=True, type=str, default="output.json"
    )

    parser.add_argument(
        "-grn_path", "--ground_truth",
        help="Gold Output file",
        required=True, type=str, default="gold_output.json"
    )

    args = parser.parse_args()

    return args


def load_json(fname):
    with open(fname, 'r') as fp:
        obj = json.load(fp)

    return obj


def score_sample(gen_out, gold_out):
    tp, fn, fp = 0, 0, 0
    metas = ['<self>', 'sil']

    for gen_tok, gold_tok in zip(
        gen_out['output_tokens'], gold_out['output_tokens']
    ):
        if gen_tok == gold_tok:
            # Correct conversion award point for non self tokens
            if gold_tok not in metas:
                tp += 1

        else:
            # Type of error
            if gold_tok in metas:
                # converted a self token
                fp += 1

            elif gen_tok in metas:
                fn += 1

            else:
                fp += 1
                fn += 1

    return tp, fn, fp


def sample_sanity_checks(gen_out, gold_out):
    errmsg = f"ERROR: SID {gen_out['sid']} in generated "\
        f"output does not match with gold SID {gold_out['sid']}."
    assert gen_out['sid'] == gold_out['sid'], errmsg

    gen_tokens = gen_out['output_tokens']
    gold_tokens = gold_out['output_tokens']

    errmsg = f"ERROR: Number of tokens {len(gen_tokens)} in generated "\
        f"output does not match with {len(gold_tokens)} in gold output "\
        f"SID {gold_out['sid']}."
    assert len(gen_tokens) == len(gold_tokens), errmsg


def score(args):
    gen_outputs = load_json(args.solution_path)
    gold_outputs = load_json(args.ground_truth)

    errmsg = f"ERROR: Number of points {len(gen_outputs)} in generated "\
        f"output does not match with gold output {len(gold_outputs)}."
    assert len(gen_outputs) == len(gold_outputs), errmsg

    tp, fn, fp = 0, 0, 0
    for idx, (gen_out, gold_out) in enumerate(zip(gen_outputs, gold_outputs)):
        sample_sanity_checks(gen_out, gold_out)
        res = score_sample(gen_out, gold_out)
        tp += res[0]
        fn += res[1]
        fp += res[2]

    prec = (1.0 * tp) / (tp + fp)
    rec = (1.0 * tp) / (tp + fn)
    f1 = (2.0 * prec * rec) / (prec + rec)

    print(
        f'Precision: {round(prec, 4)} '
        f'Recall: {round(rec, 4)} '
        f'F1: {round(f1, 4)}'
    )


if __name__ == '__main__':
    args = read_cli()
    score(args)
